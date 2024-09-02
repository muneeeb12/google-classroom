from django.shortcuts import render,redirect,get_object_or_404
from .models import Comment

# Create your views here.

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    assignment = comment.assignment
    comment.delete()
    return redirect('classroom:assignment_detail', assignment_id=assignment.id)