from django.db import models
from django.contrib.auth.models import User
from .ai_utils import analyze_fallacies

class DiscussionTopic(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    fallacy_analysis = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(DiscussionTopic, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Generate fallacy analysis when saving if content changed"""
        if not self.pk or self.content != Comment.objects.get(pk=self.pk).content:
            self.fallacy_analysis = analyze_fallacies(self.content)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.topic.title}"
