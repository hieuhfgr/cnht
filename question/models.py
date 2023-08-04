from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    is_verified = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    is_open = models.BooleanField(default=True)
    is_finished = models.BooleanField(default=False)
    
    comment_count = models.PositiveIntegerField(default=0)
    NumberOfLike = models.PositiveIntegerField(default=0)
    NumberOfDislike = models.PositiveIntegerField(default=0)
    interactiveUsers = models.JSONField(blank=True, default=dict)

    def __str__(self):
        return f"{self.title} - {self.author}: {self.is_finished}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    isHide = models.BooleanField(default=False)

    is_correct = models.BooleanField(default=False)
    NumberOfLike = models.PositiveIntegerField(default=0)
    NumberOfDislike = models.PositiveIntegerField(default=0)
    interactiveUsers = models.JSONField(blank=True, default=dict)

    is_visible = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}: {self.content}"

class MessageQnA(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    isHide = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}: {self.content}"