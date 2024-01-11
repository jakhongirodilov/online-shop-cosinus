from django.urls import path, include
from .views import SignUpView, edit_profile, logout_view, profile, add_address

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name="profile"),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('add_address', add_address, name="add_address")
]