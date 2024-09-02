from django.urls import path
from . import views
from discussion import views as discussion_views

app_name = 'classroom'

urlpatterns = [
    path('', views.list_courses, name='list_courses'),
    path('join/', views.join_classroom, name='join_classroom'),
    path('view_assignments/', views.list_user_assignments, name='view_assignments'),
    path('instructor_courses/', views.instructor_courses, name='instructor_courses'),
    path('course_creation/', views.course_creation, name='course_creation'),
    path('show_submissions/', views.show_submission, name='show_submissions'),
    path('grade_submission/<int:submission_id>/', views.grade_submission, name='grade_submission'),
    path('<int:classroom_id>/', views.classroom_detail, name='classroom_detail'),
    path('assignment/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('lecture/<int:lecture_id>/', views.lecture_detail, name='lecture_detail'),
    path('<int:classroom_id>/discussions/', discussion_views.classroom_discussions, name='classroom_discussions'),
    path('discussion/<int:topic_id>/', discussion_views.discussion_detail, name='discussion_detail'),
    path('<int:classroom_id>/create_topic/', discussion_views.create_topic, name='create_topic'),
    path('discussion/<int:topic_id>/create_post/', discussion_views.create_post, name='create_post'),
    path('post/<int:post_id>/delete/', discussion_views.delete_post, name='delete_post'),
]
