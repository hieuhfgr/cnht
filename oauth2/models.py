from django.db import models
from django.contrib.auth.models import User

# user, email,
class DiscordUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    email = models.EmailField()
    avatar = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)
    locate = models.CharField(max_length=100)
    last_login = models.DateTimeField()
    toggle_notifcation = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}"