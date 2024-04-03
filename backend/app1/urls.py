# this is app1/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('hello/', views.hello),
    path('add_client/', views.createClient),
    path('add_creator/', views.createCreator),
    path('view_roles/', views.getRoles),
    path('add_role/', views.addRole),
    path('signup/', views.PassionViewUser.as_view(), {'action': 'signup'}),
    path('login/', views.PassionViewUser.as_view(), {'action': 'login'}),
    path('reset_pass/', views.PassionViewUser.as_view(), {'action': 'reset_pass'}),
    path('profile/add/', views.add_creator_profile, name='add_creator_profile'),
    # path('signup_client/', views.PassionViewUser.as_view()),
    # path('signup_client/', views.signupClient),
    # path('signup_creator/', views.signupCreator),
]
