from django.shortcuts import render
from django.shortcuts import redirect

from .models import DiscordUser
from django.contrib.auth.models import User
from .func import exchange_code, createDiscordDatabase, Discord_last_login, Discord_login
from datetime import datetime
from .forms import RegisterForm

auth_redirect_url = "https://discord.com/api/oauth2/authorize?client_id=1090608889034178742&redirect_uri=https%3A%2F%2Fcungnhauhoctap.pythonanywhere.com%2Foauth2%2Fdiscord%2Fredirect&response_type=code&scope=identify%20email"

def home(request):
    error = request.session.get('error')
    if (request.user.is_authenticated):
        return redirect('/')
    if error != None:
        request.session.pop('error', None)
        return render(request, 'login/oauth_home.html', {"error": error})
    else:
        return redirect('/oauth2/discord')

def discord_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    return redirect(auth_redirect_url)

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    email = request.session.get('email')
    if not email:
        return redirect('/oauth2/discord')

    check_discord = DiscordUser.objects.filter(email=email)
    check_user = User.objects.filter(email=email)
    if ((len(check_discord) == 0) or (len(check_user) == 1)) and request.method != "POST":
        return redirect('/oauth2/discord')
    if (email == None):
        return redirect('/oauth2/discord')
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=form.cleaned_data['username'])
            user.email = email
            user.save()
            request.session.pop('email', None)
            if Discord_login(request, user.username):
                return redirect('/')

    return render(request, 'login/register.html', {
        'form': form,
    })

def discord_login_redirect(request):
    code = request.GET.get('code')
    if request.user.is_authenticated or (code == None):
        return redirect('/')
    Discorduser = exchange_code(code)
    if (Discorduser != False):
        if (Discorduser['verified'] == False):
            request.session['error'] = 'Bạn cần phải xác thực email trên Discord'
            return redirect('/oauth2')

        check = DiscordUser.objects.filter(id=Discorduser['id'])
        data = {
            "HasDatabase": False,
            "iscreatedAccount": False
        }
        if (len(check) != 0):
            #da tao tai khoan
            data['HasDatabase'] = True
            d_user = DiscordUser.objects.get(id=Discorduser['id']) #discord user
            if (Discorduser['email'] != d_user.email):
                request.session['error'] = 'Email Discord và Email bạn đăng kí khác nhau, Server đã cập nhật lại Email!'
                d_user.email = Discorduser['email']
                d_user.save()
                return redirect('/oauth2')

            check = User.objects.filter(email=Discorduser['email'])
            if (len(check) != 0):
                # dataotaikhoan
                user = User.objects.get(email = Discorduser['email'])
                Discord_last_login(Discorduser['id'])
                if Discord_login(request, user.username):
                    data['iscreatedAccount'] = True
                    return redirect('/')


        request.session['email'] = Discorduser['email']
        if (data["HasDatabase"] == False):
            createDiscordDatabase(Discorduser)
        if (data['iscreatedAccount'] == False):
            return redirect(f'/oauth2/register')
    else:

        return redirect(f"/register")