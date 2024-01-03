from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('submit_registration/', views.intermediate, name='submit_registration'),
    path('profile/', views.profile, name='profile'),
    path('profile/waitlist', views.waitlist, name='waitlist')
]
