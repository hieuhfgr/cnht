from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import Profile as profile
from .models import Notification as Notification
from .forms import ChangeProfileForm
from .func import is_own_page, update_top_users
from Posts.models import Post as post, Test as test
from question.models import Question

from Posts.func import get_newest_posts, get_newest_tests, markdown_to_html
from Others.func import get_website_info

def profileView(request, username):
    data = get_website_info()
    user = User.objects.get(username=username)
    ChangeNumberOfPosts_User = profile.objects.get(user=user)
    ChangeNumberOfPosts_User.NumberOfPosts = post.objects.filter(author=user, is_publish=True).values().count() + test.objects.filter(author=user, is_publish=True).values().count()
    ChangeNumberOfPosts_User.NumberOfGoodPosts = post.objects.filter(author=user, is_publish=True, is_good_post=True).values().count() + test.objects.filter(author=user, is_publish=True, is_good_test=True).values().count()
    ChangeNumberOfPosts_User.points = (ChangeNumberOfPosts_User.NumberOfGoodPosts)*2 + (ChangeNumberOfPosts_User.NumberOfPosts - ChangeNumberOfPosts_User.NumberOfGoodPosts)
    ChangeNumberOfPosts_User.save()

    posts = post.objects.filter(is_publish=True, author=user).order_by('-createdAt')[:10]
    tests = test.objects.filter(is_publish=True, author=user).order_by('-createdAt')[:10]

    data['User'] = profile.objects.get(user=user)
    data['is_own_profile'] = str(request.user.username) == str(user.username)
    data['posts'] = posts
    data['tests'] = tests
    data['questions'] = Question.objects.filter(is_published=True, author=user).order_by("-is_open")[:10]

    return render(request, 'profile/Profile.html', data)

@login_required(login_url='/login')
def profileChangeView(request):
    data = get_website_info()
    user = request.user
    userProfile = profile.objects.get(user=user)

    form = ChangeProfileForm()
    if request.method == 'POST':
        form = ChangeProfileForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['firstname']
            last_name = form.cleaned_data['lastname']
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            userProfile.name = last_name + " " + first_name
            userProfile.about = form.cleaned_data['about']
            userProfile.save()
            return HttpResponseRedirect(f'/profile/detail/{user.username}')


    form.fields['firstname'].initial = user.first_name
    form.fields['lastname'].initial = user.last_name
    form.fields['about'].initial = userProfile.about

    data['form'] = form
    return render(request, 'profile/ProfileChange.html', data)

@login_required(login_url='/login')
def profileNotification(request):
    data = get_website_info()
    user = User.objects.get(username=request.user)
    notifications = Notification.objects.filter(user = user).order_by('-createdAt')

    paginator = Paginator(notifications, 30)
    try:
        page_number = request.GET['page']
    except:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    data['notifications'] = page_obj
    return render(request, 'profile/Notification.html', data)

@login_required(login_url='/login')
def profileNotificationDelete(request):
    id = request.GET.get('id')
    if (id == None):
        return HttpResponseRedirect(f'/profile/detail/{request.user.username}')
    noti = Notification.objects.filter(id=id)
    if (len(noti) != 1):
        return HttpResponseRedirect(f'/profile/notification')
    noti = noti[0]
    if (noti.user != request.user):
        return HttpResponseRedirect(f'/profile/detail/{request.user.username}')

    noti.delete()

    return HttpRespfonseRedirect(f'/profile/notification')

@login_required(login_url='/login')
def claimRankView(request):
    data = get_website_info()
    user = request.user
    userProfile = profile.objects.get(user=user)
    userProfile.NumberOfPosts = post.objects.filter(author=user, is_publish=True).values().count() + test.objects.filter(author=user, is_publish=True).values().count()
    userProfile.NumberOfGoodPosts = post.objects.filter(author=user, is_publish=True, is_good_post=True).values().count() + test.objects.filter(author=user, is_publish=True, is_good_test=True).values().count()
    userProfile.points = (userProfile.NumberOfGoodPosts)*2 + (userProfile.NumberOfPosts - userProfile.NumberOfGoodPosts)
    userProfile.save()
    userProfile = profile.objects.get(user=user)

    result = ''
    isClaimed = False
    if request.method == 'POST':
        if (10 <= userProfile.points) and (userProfile.points < 50) and (userProfile.rank != 'C'):
            userProfile.rank = 'C'
            result = 'Bạn đã nhận được hạng <i class="fas fa-medal" style="color: #cd7f32"></i> <b>Đồng</b>!'
        elif (50 <= userProfile.points) and (userProfile.points < 200) and (userProfile.rank != 'B'):
            userProfile.rank = 'B'
            result = 'Bạn đã nhận được hạng <i class="fas fa-medal" style="color: silver"></i> <b>Bạc</b>!'
        elif (200 <= userProfile.points) and (userProfile.rank != 'A'):
            userProfile.rank = 'A'
            result = 'Bạn đã nhận được hạng <i class="fas fa-medal" style="color: gold"></i> <b>Vàng</b>!'
        else:
            result = 'Có vẻ bạn chưa nhận được hạng mới!'
        userProfile.save()
        isClaimed = True
    data['isClaimed'] = isClaimed
    data['rank'] = result
    return render(request, 'profile/claimRank.html', data)

@login_required(login_url='/login')
def redirectProfileView(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(f"/profile/detail/{request.user}")
    else:
        return HttpResponseRedirect('/login')

def searchView(request):
    data = get_website_info()
    try:
        SearchData = {
            "is_searching": True,
            "usersFound": User.objects.filter(username__icontains=request.GET['username'])
        }
    except:
        SearchData = {
            "is_searching": False,
        }
    data.update(SearchData)
    return render(request, 'profile/SearchProfile.html', data)

@login_required(login_url='/login')
def topUserListView(request):
    data = get_website_info()
    #update NumberOfPost for all users
    update_top_users()

    #pagination
    valid_users = profile.objects.filter(NumberOfPosts__gt=0).order_by('-NumberOfPosts')
    paginator = Paginator(valid_users, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data['topUsers'] = page_obj
    return render(request, 'profile/topUsers.html', data)

@login_required(login_url='/login')
def setting(request):
    data = get_website_info()
    # discorduser = DiscordUser.objects.get(email=request.user.email)
    # data['Discord_Notification'] = discorduser.toggle_notifcation

    # discord_notification = request.POST.get('Discord_notification', None)
    # if (discord_notification != None):
    #     discorduser.toggle_notifcation = not data['Discord_Notification']
    #     discorduser.save()
    #     data['Discord_Notification'] = not data['Discord_Notification']

    return render(request, 'profile/setting.html', data)