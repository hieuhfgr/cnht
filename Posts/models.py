from django.db import models
from django.contrib.auth.models import User

# Post 
class Post(models.Model):
    post_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    
    NumberOfLike = models.PositiveIntegerField(default=0)
    NumberOfDislike = models.PositiveIntegerField(default=0)
    NumberOfSeen = models.PositiveIntegerField(default=0)
    reportedCount = models.PositiveIntegerField(default=0)
    interactiveUsers = models.JSONField(blank=True, default=dict)
    tags = models.JSONField(blank=True, default=dict)

    is_verify = models.BooleanField(default=False)
    is_publish = models.BooleanField(default=False)
    is_good_post = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.post_id}. Verified: {self.is_verify}, published: {self.is_publish}"
    
# Test 
class Test(models.Model):
    test_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    NumberOfQuestions = models.PositiveIntegerField()
    NumberOfSeen = models.PositiveIntegerField(default=0)
    correctAnswers = models.JSONField(default=dict)
    reportedCount = models.PositiveIntegerField(default=0)
    userJoined = models.JSONField(blank=True, default=dict)
    tags = models.JSONField(blank=True, default=dict)

    is_verify = models.BooleanField(default=False)
    is_publish = models.BooleanField(default=False)
    is_good_test = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.test_id}. Verified: {self.is_verify}, published: {self.is_publish}"
    
class GroupTag(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.name}"
    

class Tag(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    group = models.ForeignKey(GroupTag, default=None, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} ({self.group}): {self.name}"