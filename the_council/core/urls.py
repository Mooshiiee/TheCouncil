from django.urls import path
from . import views

app_name = 'core'

# URL patterns for the core app

urlpatterns = [
    path('', views.landing, name='landing'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('home/', views.home, name='home'),
    path('settings/', views.settings, name='settings'),
    path('signout/', views.signout, name='signout'),
    path('discussions/', views.discussions, name='discussions'),
    path('discussions/<int:topic_id>/', views.discussion_detail, name='discussion_detail'),
    path('discussions/<int:topic_id>/add_comment/', views.add_comment, name='add_comment'),
    path('discussions/create/', views.create_discussion, name='create_discussion'),
]
