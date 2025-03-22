from django.urls import path
from . import views

app_name = 'core'

# URL patterns for the core app

urlpatterns = [
    path('', views.landing, name='landing'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('home/', views.home, name='home'),
    path('signout/', views.signout, name='signout'),
]
