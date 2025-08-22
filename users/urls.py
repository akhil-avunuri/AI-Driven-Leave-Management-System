from django.urls import path
from . import views  # Import views.py

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('register/', views.register, name='register'),
    path('pass_recovery/', views.pass_recovery, name='pass_recovery'),
    path('pages-404/', views.pages_404, name='pages-404'),
]
