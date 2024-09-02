from django.urls import path
from . import views

app_name = 'submission'

urlpatterns = [
    path('unsubmit/<int:submission_id>/', views.unsubmit_assignment, name='unsubmit_assignment'),
    path('grades/', views.view_student_grades, name='view_student_grades'),
]