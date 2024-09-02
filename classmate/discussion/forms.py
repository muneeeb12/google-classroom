from django import forms
from .models import DiscussionTopic, DiscussionPost

class DiscussionTopicForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter topic title',
        'class': 'w-full py-4 px-6 rounded mb-2'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Enter topic description',
        'class': 'w-full py-4 px-6 rounded mb-2',
        'rows': 4
    }))

    class Meta:
        model = DiscussionTopic
        fields = ['title', 'description']

class DiscussionPostForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Type your message here',
        'class': 'w-full py-4 px-6 rounded mb-2',
        'rows': 3
    }))

    class Meta:
        model = DiscussionPost
        fields = ['message']
