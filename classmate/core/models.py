from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)    

    def __str__(self):
        return self.user.username
