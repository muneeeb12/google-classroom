from django import forms
from .models import Comment  # Import the Comment model

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 1.5,
                'placeholder': 'Add a comment...',
                'class': 'w-full bg-gray-100 border rounded-md py-2 px-4 leading-tight focus:outline-none focus:bg-white focus:border-blue-500'
            })
        }
