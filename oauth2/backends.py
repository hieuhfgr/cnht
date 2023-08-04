from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User as UserModel

class UsernameBackend(BaseBackend):
    def authenticate(self, request, username=None, **kwargs):
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None

        return user

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None