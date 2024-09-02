from django import forms
from django.forms import ModelForm
from .models import Classroom,Assignment,Lecture
from submission.models import Grade
from django.utils.crypto import get_random_string

# Generate a unique classroom code
def generate_unique_code(length=8):
    return get_random_string(length=length, allowed_chars='1234567890')

# Enhanced Classroom Creation Form
class ClassroomCreationForm(ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Classroom Title',
            'class': 'w-full py-4 px-6 rounded mb-2'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Brief description of the classroom',
            'class': 'w-full py-4 px-6 rounded mb-2',
            'rows': 2
        })
    )
    code = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Classroom Code',
            'class': 'w-full py-4 px-6 rounded mb-2',
            'readonly': 'readonly'  # Make it read-only
        }),
        initial=generate_unique_code()
    )

    class Meta:
        model = Classroom
        fields = ['title', 'description', 'code']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.pk or not instance.code:
            instance.code = generate_unique_code()
        if commit:
            instance.save()
        return instance


class AssignmentCreationForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Assignment Title',
            'class': 'w-full py-3 px-5 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Brief description of the assignment',
            'class': 'w-full py-3 px-5 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4',
            'rows': 2
        })
    )
    file = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={
            'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-white focus:outline-none mb-4'
        })
    )
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full py-3 px-5 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4'
        })
    )
    total_marks = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter Total Marks',
            'class': 'w-full py-3 px-5 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4',
            'min': 0,
            'max':10,
            'step': 1
        })
    )

    class Meta:
        model = Assignment
        fields = ['title', 'total_marks', 'description', 'file', 'due_date']


class LectureCreationForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Lecture Title',
            'class': 'w-full py-3 px-5 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4'
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Brief description of the lecture (optional)',
            'class': 'w-full py-3 px-5 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4',
            'rows': 2
        })
    )
    content_file = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={
            'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-white focus:outline-none mb-4'
        })
    )

    class Meta:
        model = Lecture
        fields = ['title', 'description', 'content_file']



class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['grade', 'remarks']
        widgets = {
            'grade': forms.NumberInput(attrs={
                'class': 'w-full py-2 px-4 border rounded-lg mb-2',
                'min': 0,
                'step': 0.01
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'w-full py-2 px-4 border rounded-lg mb-2',
                'rows': 3,
                'placeholder': 'Enter remarks (optional)'
            }),
        }