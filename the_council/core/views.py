from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import DiscussionTopic

def landing(request):
    return render(request, 'core/landing.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:home')
        else:
            # Return an 'invalid login' error message.

            # Pass an empty form object so the context has a form to reference
            return render(request, 'core/signin.html', {'error_message': 'Invalid login credentials'})
    else:

        # Pass an empty form object so the context has a form to reference
        return render(request, 'core/signin.html')

def home(request):
    discussion_topics = DiscussionTopic.objects.all().order_by('-created_at')
    return render(request, 'core/home.html', {'discussion_topics': discussion_topics, 'user': request.user})

def signout(request):
    logout(request)
    return redirect('core:landing')
