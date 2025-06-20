from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import User


def create_user(request):
    """
    Simple view for creating a user
    """
    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        role = request.POST.get('role', User.Role.USER)
        
        # Basic validation
        if not all([email, first_name, last_name, password]):
            messages.error(request, 'All fields are required.')
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
