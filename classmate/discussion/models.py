from django.db import models
from core.models import UserProfile
from classroom.models import Classroom 

class DiscussionTopic(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='discussion_topics')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} in {self.classroom.title}"

class DiscussionPost(models.Model):
    topic = models.ForeignKey(DiscussionTopic, on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.user.username} in topic {self.topic.title}"
