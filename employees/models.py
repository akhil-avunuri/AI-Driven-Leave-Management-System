from django.db import models
from admin_role.models import department, leave

# Create your models here.    
class leaveapplication(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    employee_id = models.CharField(max_length=20)
    employee_name = models.CharField(max_length=100)
    department = models.ForeignKey(department, on_delete=models.SET_NULL, null=True, blank=True)  
    leave_type = models.ForeignKey(leave, on_delete=models.PROTECT)
    leave_description = models.TextField()
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    # employee_email = models.EmailField()

    def __str__(self):
        return (f"{self.employee_name} ({self.employee_id})")


