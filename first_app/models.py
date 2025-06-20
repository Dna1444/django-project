from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', self.model.Role.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    
    Fields in this model:
    
    CUSTOM FIELDS:
    - email: EmailField (unique, used as username)
    - first_name: CharField (max_length=30)
    - last_name: CharField (max_length=30)
    - role: CharField with choices (admin/user)
    - created_at: DateTimeField (auto_now_add=True)
    - updated_at: DateTimeField (auto_now=True)
    
    INHERITED FIELDS FROM AbstractUser:
    - password: CharField (hashed password)
    - is_active: BooleanField (default=True)
    - is_staff: BooleanField (default=False)
    - is_superuser: BooleanField (default=False)
    - last_login: DateTimeField (nullable)
    - date_joined: DateTimeField (auto_now_add=True)
    - groups: ManyToManyField to Group
    - user_permissions: ManyToManyField to Permission
    
    OVERRIDDEN FIELDS:
    - username: Set to None (using email instead)
    """
    
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'
    
    # Override username field to use email instead
    username = None
    email = models.EmailField(unique=True)
    
    # Custom fields
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Inherited fields from AbstractUser include:
    # - password (hashed)
    # - is_active, is_staff, is_superuser
    # - last_login, date_joined
    # - groups, user_permissions
    
    # Use email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    # Use our custom manager
    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
