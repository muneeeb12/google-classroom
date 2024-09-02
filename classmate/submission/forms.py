from django import forms
from .models import Submission

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = [ 'file']
        

    file = forms.FileField(widget=forms.FileInput(attrs={
        'placeholder': 'File',
        'class': 'w-full py-4 px-6 rounded mb-2'
        }))