# this is app1/urls.py

from django.urls import path

from . import views

urlpatterns = [

path('hello/', views.hello),
path('add_client/', views.createClient),
path('add_creator/', views.createCreator),
path('signup_client/', views.signupClient),
path('signup_creator/', views.signupCreator),
]
