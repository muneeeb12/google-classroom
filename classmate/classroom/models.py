from django.db import models
from django.utils.crypto import get_random_string
from core.models import UserProfile


def generate_unique_code():
    return get_random_string(length=8, allowed_chars='1234567890')

class Classroom(models.Model):
    instructor = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.title

    def enrolled_students(self):
        students = UserProfile.objects.filter(enrollment__classroom=self)
        return students
    
    def generate_code(self):
        self.code = generate_unique_code()
        self.save()

class Lecture(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    content_file = models.FileField(upload_to='lectures/')

    def __str__(self):
        return self.title

class Assignment(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    is_done = models.BooleanField(default=False)  
    file = models.FileField(upload_to='assignments/', blank=True, null=True) 
    total_marks = models.FloatField(default=0)

    def __str__(self):
        return self.title
    
    def get_total_marks(self):
        if self.total_marks == 0:
            return "Not Graded"
        return self.total_marks

class Enrollment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enrollment: {self.user} - {self.classroom.title}"
