from django.urls import path
from . import views

urlpatterns = [
    path('leave_form/', views.leave_form, name='leave_form'),
    path('apply_leave/', views.apply_leave, name='apply_leave'),
    path('get_probability_score/', views.get_probability_score, name='get_probability_score'),  # New API route
    path('test_gemini_api/', views.test_gemini_api, name='test_gemini_api'),  # Test endpoint - supports both GET and POST
    path('test_gemini/', views.test_gemini_api, name='test_gemini'),  # Alias for GET access
    path('schedules/', views.schedules, name='schedules'),
]
