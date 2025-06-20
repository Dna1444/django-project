#!/usr/bin/env python
"""
Script to show all fields in the User model
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_project.settings')
django.setup()

from first_app.models import User

# Get all field names
field_names = [field.name for field in User._meta.get_fields()]

print("User model fields:")
print("=" * 50)
for i, field_name in enumerate(field_names, 1):
    print(f"{i:2d}. {field_name}")

print("\n" + "=" * 50)
print(f"Total fields: {len(field_names)}") 