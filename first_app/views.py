from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
import re
from .models import User


def sanitize_input(text):
    """Sanitize user input to prevent XSS and injection attacks"""
    if not text:
        return ""
    # Remove HTML tags
    text = strip_tags(text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def validate_user_input(email, first_name, last_name, password):
    """Comprehensive validation for user input"""
    errors = []
    
    # Email validation
    try:
        validate_email(email)
    except ValidationError:
        errors.append("Please enter a valid email address.")
    
    # Name validation
    if not first_name or len(first_name.strip()) < 2:
        errors.append("First name must be at least 2 characters long.")
    elif len(first_name) > 30:
        errors.append("First name cannot exceed 30 characters.")
    elif not re.match(r'^[a-zA-Z\s\-\.]+$', first_name):
        errors.append("First name can only contain letters, spaces, hyphens, and periods.")
    
    if not last_name or len(last_name.strip()) < 2:
        errors.append("Last name must be at least 2 characters long.")
    elif len(last_name) > 30:
        errors.append("Last name cannot exceed 30 characters.")
    elif not re.match(r'^[a-zA-Z\s\-\.]+$', last_name):
        errors.append("Last name can only contain letters, spaces, hyphens, and periods.")
    
    # Password validation
    if not password or len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    elif len(password) > 128:
        errors.append("Password cannot exceed 128 characters.")
    elif not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter.")
    elif not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter.")
    elif not re.search(r'\d', password):
        errors.append("Password must contain at least one number.")
    
    return errors


def create_user(request):
    """
    Simple view for creating a user with enhanced security
    """
    if request.method == 'POST':
        # Get and sanitize form data
        email = sanitize_input(request.POST.get('email', ''))
        first_name = sanitize_input(request.POST.get('first_name', ''))
        last_name = sanitize_input(request.POST.get('last_name', ''))
        password = request.POST.get('password', '')  # Don't sanitize password
        role = request.POST.get('role', User.Role.USER)
        
        # Validate role
        if role not in [User.Role.USER, User.Role.ADMIN]:
            role = User.Role.USER
        
        # Comprehensive validation
        validation_errors = validate_user_input(email, first_name, last_name, password)
        
        if validation_errors:
            for error in validation_errors:
                messages.error(request, error)
            return render(request, 'first_app/create_user.html')
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'A user with this email already exists.')
            return render(request, 'first_app/create_user.html')
        
        try:
            # Create the user
            user = User.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                role=role
            )
            messages.success(request, f'User {user.first_name} {user.last_name} created successfully!')
            return redirect('/admin/first_app/user/')  # Redirect to admin user list
            
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
            return render(request, 'first_app/create_user.html')
    
    # GET request - show the form
    return render(request, 'first_app/create_user.html')
