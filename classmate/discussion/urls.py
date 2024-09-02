from django.urls import path
from . import views

urlpatterns = [
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('delete_topic/<int:post_id>/', views.delete_topic, name='delete_topic'),
]