from django import forms
from .models import DiscussionTopic, Comment

class DiscussionTopicForm(forms.ModelForm):
    class Meta:
        model = DiscussionTopic
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'parent_comment']
        widgets = {
            'parent_comment': forms.HiddenInput(),
        }
