from django import forms
from .models import DiscussionTopic

class DiscussionTopicForm(forms.ModelForm):
    class Meta:
        model = DiscussionTopic
        fields = ['title', 'content']
