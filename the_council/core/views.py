from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import DiscussionTopic, Comment
from .forms import DiscussionTopicForm

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
    # This view is for settings and a link to the discussions page
    return render(request, 'core/home.html', {'user': request.user})


def settings(request):
    return render(request, 'core/settings.html')


def discussions(request):
    discussion_topics = DiscussionTopic.objects.all().order_by('-created_at')
    return render(request, 'core/discussions.html', {'discussion_topics': discussion_topics})


@login_required
def discussion_detail(request, topic_id):
    discussion = get_object_or_404(DiscussionTopic, pk=topic_id)
    comments = Comment.objects.filter(topic=discussion, parent_comment=None).order_by('created_at')  # Get only top-level comments
    return render(request, 'core/discussion_detail.html', {'discussion': discussion, 'comments': comments})


@login_required
def add_comment(request, topic_id):
    discussion = get_object_or_404(DiscussionTopic, pk=topic_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        parent_comment_id = request.POST.get('parent_comment_id')  # Get the parent comment ID if it exists

        if parent_comment_id:
            parent_comment = get_object_or_404(Comment, pk=parent_comment_id)
            Comment.objects.create(content=content, author=request.user, topic=discussion, parent_comment=parent_comment)
        else:
            Comment.objects.create(content=content, author=request.user, topic=discussion)
        return redirect('core:discussion_detail', topic_id=topic_id)
    # Redirect to discussion detail even if it's not a POST request
    return redirect('core:discussion_detail', topic_id=topic_id)


@login_required
def create_discussion(request):
    if request.method == 'POST':
        form = DiscussionTopicForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.author = request.user
            discussion.save()
            return redirect('core:discussion_detail', topic_id=discussion.id)
    else:
        form = DiscussionTopicForm()
    return render(request, 'core/create_discussion.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('core:landing')
