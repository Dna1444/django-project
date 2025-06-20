from django.urls import path
from . import views

app_name = 'first_app'

urlpatterns = [
    path('users/create/', views.create_user, name='create_user'),
] 