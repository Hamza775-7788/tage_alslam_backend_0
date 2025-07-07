from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import get_governments ,  get_regions , create_user , get_profile,sign_in,update_profile,update_password




urlpatterns = [
    path('gov/', get_governments),
    path('regions/<pk>/', get_regions),
    path('profile/', get_profile),  # Assuming this is meant to get a profile by user ID
    path('update-profile/', update_profile),  # Assuming this is meant to get a profile by user ID
    path('create_user/', create_user),
    path('sign-in/', sign_in),
    path('change-passowrd/', update_password),

    # path('regions/', get_regions),  # This line is commented out as it seems redundant
]
