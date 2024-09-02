from django.shortcuts import render, redirect,get_object_or_404
from .models import Submission,Grade

def unsubmit_assignment(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    
    if request.user.is_authenticated and submission.student.user == request.user:
        submission.delete()
        redirect('classroom:classroom_detail', classroom_id=submission.assignment.classroom.id)

    return redirect('classroom:classroom_detail', classroom_id=submission.assignment.classroom.id)

def view_student_grades(request):
    user_profile = request.user.profile  
    grades = Grade.objects.filter(student=user_profile).select_related('submission', 'submission__assignment')
    return render(request, 'submission/student_grades.html', {'grades': grades})