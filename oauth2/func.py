from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from cungnhauhoctap.settings import conf

class EmailBackend(ModelBackend):
    def Discord_authenticate(self, request, email=None, **kwargs):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None

import requests
def exchange_code(code):
    data = {
        "client_id" : "1090608889034178742",
        "client_secret": "OCQN4lqiVfU7TC52ymukBpLPRkUAM6Mk",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": f"{conf['website_URL']}oauth2/discord/redirect",
        "scope": "identify email"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    credentials = response.json()
    print(credentials)
    try:
        access_token = credentials['access_token']
        print(f"access_token: {access_token}")
        response = requests.get('https://discord.com/api/v10/users/@me', headers={
            "Authorization": "Bearer %s" %access_token
        })
        user = response.json()
        return user
    except:
        return False

from .models import DiscordUser
from datetime import datetime
def createDiscordDatabase(user):
    DiscordUser.objects.create(
            id=user['id'],
            email=user['email'],
            avatar=f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png",
            locate=user['locale'],
            last_login=datetime.now(),
        )

def Discord_last_login(id):
    DiscordUser.objects.get(id=id).last_login = datetime.now()

from django.contrib.auth import authenticate, login
def Discord_login(request, username):
    user = authenticate(username=username)
    if user is not None:
        login(request, user)
        return True
    else:
        return False