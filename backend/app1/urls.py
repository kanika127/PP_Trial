# this is app1/urls.py

from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views, my_views

urlpatterns = [
    path('hello/', my_views.temptesting_views.hello),
    # path('add_client/', my_views.temptesting_views.createClient),
    # path('add_creator/', my_views.temptesting_views.createCreator),
    # path('view_roles/', my_views.temptesting_views.getRoles),
    # path('add_role/', my_views.temptesting_views.addRole),
    # path('application/', my_views.temptesting_views.createApplication),
    # path('signup/', views.PassionViewUser.as_view(), {'action': 'signup'}),
    path('login/', views.PassionViewUser.as_view(), {'action': 'login'}),
    path('reset_pass/', views.PassionViewUser.as_view(), {'action': 'reset_pass'}),
    # path('profile/add/', views.add_creator_profile, name='add_creator_profile'),
    path('check_username/', views.UserRegistrationView.as_view(), {'action': 'check_username'}),
    path('register/', views.UserRegistrationView.as_view(), {'action': 'register'}, name='register'),
    path('verify-email/', views.EmailVerifyView.as_view(), name='email-verify'),
    path('email_verify/', views.EmailVerifyView.as_view(), name='email-verify'),
    path('verify_phone_number/', views.UserRegistrationView.verify_phone_number, name='verify_phone_number'),

    path('add_creator_field/', views.PassionViewUser.as_view(), {'action': 'add_creator_field'}),
    path('add_client_industry/', views.PassionViewUser.as_view(), {'action': 'add_client_industry'}),

    path('edit_creator/', views.PassionViewUser.as_view(), {'action': 'edit_creator'}),

    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    path('add_project/', views.ProjectCreateAPIView.as_view(), name='add_project'),
    # path('add_project/', views.ProjectCreateAPIView.as_view(), {'action': 'add_project'}),
    path('my-pitched-projects/', views.UserProjectsView.as_view(), name='my-pitched-projects'),
    path('my-applications/', views.UserApplicationsAPIView.as_view(), name='my-applications'),
    path('my-past-projects/', views.UserPastProjectsView.as_view(), name='my-past-projects'),
    path('projects', views.ProjectListCreateAPIView.as_view()),
    path('projects/detail/<int:id>', views.Project_Retrieve_Update_Destroy_View.as_view(), name='project-details'),
    path('applications', views.ApplicationListCreateAPIView.as_view()),
    path('projectboard/', views.ProjectBoardDisplay.as_view(), {'action': 'project-board'}),
]
