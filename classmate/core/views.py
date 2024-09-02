from django.shortcuts import render,redirect
from .models import UserProfile
from .forms import UserProfileForm,LoginForm
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render(request, 'core/home.html')

def dashboard(request):
    try:
        userprofile = request.user.profile  # Accessing the related UserProfile using 'profile' attribute
    except UserProfile.DoesNotExist:
        userprofile = None

    return render(request, 'core/dashboard.html', {'userprofile': userprofile})


def signup(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username, password=request.POST['password1'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = UserProfileForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Correct usage of login function
                return redirect('dashboard')  # Redirect to the homepage after successful login
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
