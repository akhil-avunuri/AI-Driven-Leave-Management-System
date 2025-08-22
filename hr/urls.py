from django.urls import path
from . import views

urlpatterns = [
    path('leave_list/', views.leave_list, name='leave_list'),
    path('leave_description/<int:leave_id>/', views.leave_description, name='leave_description'),
    path('update_leave_status/<int:leave_id>/<str:status>/', views.update_leave_status, name='update_leave_status'),
]
