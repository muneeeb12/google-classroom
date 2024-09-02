from django.shortcuts import render,redirect,get_object_or_404
from .models import Classroom, Assignment, Lecture, Enrollment
from django.contrib import messages
from submission.models import Submission,Grade
from submission.forms import SubmissionForm
from comment.models import Comment
from comment.forms import CommentForm
from django.utils import timezone
from .forms import ClassroomCreationForm,AssignmentCreationForm,LectureCreationForm,GradeForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def list_courses(request):
    userprofile = request.user.profile
    enrolled_classes = Enrollment.objects.filter(user=userprofile)
    return render(request, 'classroom/list_courses.html', {'enrolled_classes': enrolled_classes})


def join_classroom(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        if code:
            try:
                classroom = Classroom.objects.get(code=code)
                user_profile = request.user.profile
                
                # Check if the user is already enrolled in the classroom
                if Enrollment.objects.filter(user=user_profile, classroom=classroom).exists():
                    messages.warning(request, "You are already enrolled in this classroom.")
                else:
                    # Enroll the user in the classroom
                    Enrollment.objects.create(user=user_profile, classroom=classroom)
                    messages.success(request, "You have successfully joined the classroom.")
                
                # Redirect back to the list of courses
                return redirect('classroom:list_courses')

            except Classroom.DoesNotExist:
                messages.error(request, "Classroom not found. Please enter a valid code.")

    # If code is not provided or enrollment fails, redirect back to the join classroom page
    return redirect('join_classroom')


def classroom_detail(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    lectures = Lecture.objects.filter(classroom=classroom)
    assignments = Assignment.objects.filter(classroom=classroom)
    classroom_students = classroom.enrolled_students()

    is_instructor = request.user.is_authenticated and request.user.profile == classroom.instructor
    assignment_creation_form = LectureCreationForm() if is_instructor else None
    lecture_creation_form = LectureCreationForm() if is_instructor else None

    if not classroom_students:
        messages.info(request, "No students are currently enrolled in this classroom.")

    if request.method == 'POST':
        if is_instructor:
            if 'submit_assignment' in request.POST:
                assignment_creation_form = AssignmentCreationForm(request.POST, request.FILES)
                if assignment_creation_form.is_valid():
                    new_assignment = assignment_creation_form.save(commit=False)
                    new_assignment.classroom = classroom
                    new_assignment.save()
                    messages.success(request, "Assignment created successfully!")
                    return redirect('classroom:classroom_detail', classroom_id=classroom_id)
                else:
                    messages.error(request, "There was an issue creating the assignment. Please check the form.")
            elif 'submit_lecture' in request.POST:
                lecture_creation_form = LectureCreationForm(request.POST, request.FILES)
                if lecture_creation_form.is_valid():
                    new_lecture = lecture_creation_form.save(commit=False)
                    new_lecture.classroom = classroom
                    new_lecture.save()
                    messages.success(request, "Lecture created successfully!")
                    return redirect('classroom:classroom_detail', classroom_id=classroom_id)
                else:
                    messages.error(request, "There was an issue creating the lecture. Please check the form.")

    context = {
        'classroom': classroom,
        'lectures': lectures,
        'assignments': assignments,
        'classroom_students': classroom_students,
        'is_instructor': is_instructor,
        'assignment_creation_form': assignment_creation_form,
        'lecture_creation_form': lecture_creation_form
    }

    return render(request, 'classroom/classroom_detail.html', context)

def lecture_detail(request, lecture_id):
    lecture = Lecture.objects.get(id=lecture_id)
    return render(request, 'classroom/lecture_detail.html', {'lecture': lecture})

def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submission_form = SubmissionForm()
    comment_form = CommentForm()  # Instance of the comment form
    comments = Comment.objects.filter(assignment=assignment)  # Fetch comments related to the assignment
    submission_exists = False  # Default value for submission existence check
    existing_submission = None

    if request.user.is_authenticated:
        user_profile = request.user.profile
        existing_submission = Submission.objects.filter(assignment=assignment, student=user_profile).first()
        if existing_submission:
            submission_exists = True

    if request.method == 'POST':
        if 'submit_assignment' in request.POST:
            submission_form = SubmissionForm(request.POST, request.FILES)
            if submission_form.is_valid():
                # Save the submission
                new_submission = submission_form.save(commit=False)
                new_submission.assignment = assignment
                new_submission.student = user_profile
                new_submission.save()
                messages.success(request, "Your submission has been uploaded successfully.")
                return redirect('classroom:assignment_detail', assignment_id=assignment_id)
        elif 'add_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.assignment = assignment
                new_comment.user = user_profile
                new_comment.save()
                return redirect('classroom:assignment_detail', assignment_id=assignment_id)

    context = {
        'assignment': assignment,
        'submission_form': submission_form,
        'comment_form': comment_form,
        'comments': comments,
        'submission_exists': submission_exists,
        'existing_submission': existing_submission
    }
    return render(request, 'classroom/assignment_detail.html', context)

@login_required
def list_user_assignments(request):
    user_profile = request.user.profile
    now = timezone.now()  # Ensure timezone-aware comparison
    classrooms = Classroom.objects.filter(enrollment__user=user_profile)
    assignments = Assignment.objects.filter(classroom__in=classrooms).order_by('due_date')
    
    todo_assignments = []
    submitted_assignments = []
    missing_assignments = []
    
    for assignment in assignments:
        submission = Submission.objects.filter(assignment=assignment, student=user_profile).first()
        if submission:
            submitted_assignments.append(assignment)
        elif assignment.due_date < now.date():
            missing_assignments.append(assignment)
        else:
            todo_assignments.append(assignment)
    
    return render(request, 'classroom/user_assignments.html', {
        'todo_assignments': todo_assignments,
        'submitted_assignments': submitted_assignments,
        'missing_assignments': missing_assignments,
    })

def instructor_courses(request):
    user_profile = request.user.profile
    classrooms = Classroom.objects.filter(instructor=user_profile)
    return render(request, 'classroom/instructor_courses.html', {'classrooms': classrooms})

def course_creation(request):

    form = ClassroomCreationForm()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        code = request.POST.get('code')
        user_profile = request.user.profile

        # Check if the code is already in use
        if Classroom.objects.filter(code=code).exists():
            messages.error(request, "Classroom code already in use. Please choose a different code.")
            return redirect('classroom:course_creation')

        # Create the classroom
        classroom = Classroom.objects.create(title=title, description=description, code=code, instructor=user_profile)
        messages.success(request, "Classroom created successfully.")
        return redirect('classroom:classroom_detail', classroom_id=classroom.id)

    return render(request, 'classroom/course_creation.html', {'form': form})

def show_submission(request):
    user_profile = request.user.profile
    classrooms = Classroom.objects.filter(instructor=user_profile)
    classroom_submissions = {}

    for classroom in classrooms:
        submissions = Submission.objects.filter(assignment__classroom=classroom)
        classroom_submissions[classroom] = submissions

    return render(request, 'classroom/show_submission.html', {'classroom_submissions': classroom_submissions})

def grade_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    
    try:
        grade_instance = Grade.objects.get(submission=submission, student=submission.student)
    except Grade.DoesNotExist:
        grade_instance = None

    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade_instance)
        if form.is_valid():
            grade_instance = form.save(commit=False)
            if not grade_instance.pk:
                grade_instance.submission = submission
                grade_instance.student = submission.student
            grade_instance.save()

            submission.is_graded = True
            submission.save()

            messages.success(request, "The grade has been successfully updated.")
            return redirect('classroom:show_submissions')
    else:
        form = GradeForm(instance=grade_instance)

    return render(request, 'classroom/grade_submission.html', {
        'form': form,
        'submission': submission,
        'grade': grade_instance
    })