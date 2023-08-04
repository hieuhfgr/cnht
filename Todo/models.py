from django.db import models
from django.db import models
from django.contrib.auth.models import User

class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    detail = models.CharField(max_length=255, default="")
    
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user} {self.title}"

class ToDo_GroupUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_user = models.JSONField(blank=True, default=dict)
    #access_user: {username, firstname}
    title = models.CharField(max_length=255)
    detail = models.CharField(max_length=255, default="")
    
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user} {self.title}"