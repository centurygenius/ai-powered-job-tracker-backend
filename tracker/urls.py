from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
    path('job-applications/', views.JobApplicationView.as_view(), name='job-applications'),
    path('job-applications/<int:pk>/', views.JobApplicationDetail.as_view(), name='job-application-detail'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('resume-feedback/', views.resume_feedback),
    path('job-recommendations/', views.job_recommendations),
]