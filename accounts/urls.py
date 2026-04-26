from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/embed/', views.signup_embed, name='signup_embed'),
    path('profile/', views.profile, name='profile'),
]
