from django.db import models
from core.models import UserProfile
from classroom.models import Lecture, Assignment

class Comment(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
    class Meta:
        ordering = ['-created_at']