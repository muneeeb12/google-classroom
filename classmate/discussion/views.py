from django.shortcuts import render,get_object_or_404,redirect
from django.core.exceptions import PermissionDenied
from classroom.models import Classroom
from .models import DiscussionTopic, DiscussionPost
from .forms import DiscussionTopicForm, DiscussionPostForm


def classroom_discussions(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    topics = classroom.discussion_topics.all()
    context = {
        'classroom': classroom,
        'topics': topics
    }
    return render(request, 'discussion/discussions.html', context)

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import DiscussionTopic, DiscussionPost
from .forms import DiscussionPostForm

def discussion_detail(request, topic_id):
    topic = get_object_or_404(DiscussionTopic, id=topic_id)
    posts = topic.posts.all()
    form = DiscussionPostForm()  # Initialize an empty form for GET requests

    if request.method == 'POST':
        form = DiscussionPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.topic = topic
            new_post.user = request.user.profile  # Ensure this aligns with your user profile setup
            new_post.save()
            messages.success(request, "Post added successfully.")
            return redirect('classroom:discussion_detail', topic_id=topic.id)

    context = {
        'topic': topic,
        'posts': posts,
        'form': form
    }
    return render(request, 'discussion/discussion_detail.html', context)


def create_topic(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    if request.method == 'POST':
        form = DiscussionTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.classroom = classroom
            topic.save()
            return redirect('classroom:classroom_discussions', classroom_id=classroom.id)
    else:
        form = DiscussionTopicForm()
    context = {
        'form': form,
        'classroom': classroom
    }
    return render(request, 'discussion/create_topic.html', context)

def create_post(request, topic_id):
    topic = get_object_or_404(DiscussionTopic, id=topic_id)
    if request.method == 'POST':
        form = DiscussionPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.user = request.user.profile  # Ensure UserProfile is linked to User
            post.save()
            return redirect('classroom:discussion_detail', topic_id=topic.id)
    else:
        form = DiscussionPostForm()
    context = {
        'form': form,
        'topic': topic
    }
    return render(request, 'discussion/create_post.html', context)


def delete_post(request, post_id):
    post = get_object_or_404(DiscussionPost, id=post_id)
    topic_id = post.topic.id
    post.delete()
    return redirect('classroom:discussion_detail', topic_id=topic_id)

def delete_topic(request, topic_id):
    topic = get_object_or_404(DiscussionTopic, id=topic_id)
    classroom_id = topic.classroom.id
    topic.delete()
    return redirect('classroom:classroom_discussions', classroom_id=classroom_id)