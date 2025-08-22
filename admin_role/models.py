from django.db import models

# Create your models here.
class department(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    department_name = models.CharField(max_length=100)
    num_of_subjects = models.IntegerField()

    def __str__(self):
        return (f"{self.department_name}")
    
class faculty(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    faculty_id = models.CharField(max_length=20, unique=True)
    faculty_name = models.CharField(max_length=100)
    email_id = models.EmailField(unique=True)
    subject = models.CharField(max_length=100)
    department = models.ForeignKey(department, on_delete=models.SET_NULL, null=True, blank=True)  

    def __str__(self):
        return (f"{self.faculty_name} ({self.faculty_id})")

class hod(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hod_id = models.CharField(max_length=20, unique=True)
    hod_name = models.CharField(max_length=100)
    email_id = models.EmailField(unique=True)
    subject = models.CharField(max_length=100)
    department = models.ForeignKey(department, on_delete=models.SET_NULL, null=True, blank=True)  

    def __str__(self):
        return (f"{self.hod_name} ({self.hod_id})")
    
# class subject(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     subject_name = models.CharField(max_length=100)
#     department = models.ForeignKey(department, on_delete=models.CASCADE, null=True, blank=True)  # Set null=True temporarily

#     def __str__(self):
#         return self.subject_name
    
class leave(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    leave_name = models.CharField(max_length=100)
    def __str__(self):
        return (f"{self.leave_name}")

class Schedule(models.Model):
    section_name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    faculty = models.ForeignKey('faculty', on_delete=models.CASCADE, null=True, blank=True, related_name='schedules')
    is_replacement = models.BooleanField(default=False)
    replaced_faculty = models.ForeignKey('faculty', on_delete=models.SET_NULL, null=True, blank=True, related_name='replacements')

    def __str__(self):
        return self.section_name 