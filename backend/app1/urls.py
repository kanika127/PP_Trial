# this is app1/urls.py

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views, my_views

urlpatterns = [
    # path('hello/', my_views.temptesting_views.hello),
    # path('add_client/', my_views.temptesting_views.createClient),
    # path('add_creator/', my_views.temptesting_views.createCreator),
    # path('view_roles/', my_views.temptesting_views.getRoles),
    # path('add_role/', my_views.temptesting_views.addRole),
    # path('application/', my_views.temptesting_views.createApplication),
    # path('signup/', views.PassionViewUser.as_view(), {'action': 'signup'}),

    # Kanika
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
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
    #path('add_project/', views.ProjectCreateAPIView.as_view(), name='add_project'),
    # path('add_project/', views.ProjectCreateAPIView.as_view(), {'action': 'add_project'}),
    #path('projects/detail/<int:id>', views.Project_Retrieve_Update_Destroy_View.as_view(), name='project-details'),
  
    # path('projectboard/', views.ProjectBoardDisplay.as_view(), {'action': 'project-board'}),

    # path('projects/<int:pk>/', views.ProjectDetailAPIView.as_view()),  # For GET, PUT, DELETE on a single project
    # path('projects/<int:pk>/', views.ProjectRetrieveUpdateDestroyAPIView.as_view()),  # For GET, PUT, DELETE on a single project

    # Vandana
    path('projects/', views.ProjectListCreateAPIView.as_view()),
    # path('projects/owner/<str:username>/', views.ProjectListByOwnerAPIView.as_view(), name='project-list-by-owner'),
    # path('projects/detail/owner/<int:id>/', views.ProjectOwnerView.as_view(), name='project-details-owner'),
    path('dashboard/live_projects/<str:username>/', views.LiveProjectListByOwnerAPIView.as_view(), name='live-project-list-by-owner'),
    path('dashboard/past_projects/<str:username>/', views.PastProjectListByOwnerAPIView.as_view(), name='past-project-list-by-owner'),
    path('dashboard/application/<str:username>/', views.ApplicationListByOwnerAPIView.as_view(), name='application-list-by-owner'),
    path('dashboard/project_detail/<int:id>/', views.ProjectOwnerView.as_view(), name='project-details-owner'),
    path('projects/detail/applicant/<int:id>/', views.ProjectApplicantView.as_view(), name='project-detailsapplicant'),
    path('projects/search/', views.ProjectSearchListView.as_view(), name='project-search'),
    path('projects/filter/', views.ProjectCreateFilterView.as_view(), name='project-filter'),
    path('projects/filter/apply/', views.ProjectFilteredListView.as_view(), name='project-filter-search'),
    path('projects/delete/', views.ProjectRetrieveUpdateDestroyView.as_view(), name='project-delete'),

    path('applications/', views.ApplicationListCreateAPIView.as_view()),
]
