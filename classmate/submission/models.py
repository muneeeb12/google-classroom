from django.db import models
from core.models import UserProfile
from classroom.models import Assignment 
from django.core.exceptions import ValidationError


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/')
    is_graded = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.assignment} - {self.student}'
    
    @property
    def grade_instance(self):
        grade_instance = Grade.objects.filter(submission=self).first()
        return grade_instance.grade
        


class Grade(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    grade = models.FloatField()
    remarks = models.TextField(blank=True, null=True)

    def clean(self):
        """Custom validation for the grade field."""
        if self.grade is not None:
            if self.grade < 0 or (self.submission and self.grade > self.submission.assignment.total_marks):
                raise ValidationError(f"Grade must be between 0 and {self.submission.assignment.total_marks}")
        else:
            raise ValidationError("Grade cannot be None.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.submission} - {self.student} - {self.grade}'
