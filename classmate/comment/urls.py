from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]