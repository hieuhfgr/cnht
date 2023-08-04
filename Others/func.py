from django.contrib.auth.models import User
from Todo.models import ToDo
from Profile.models import Profile as member
from Profile.models import Notification as Notification
from Home.models import Announcement, BadWord
from Posts.models import Post, Test
from django.http import HttpResponseRedirect

import re
from markdown import markdown
import requests
import json
from cungnhauhoctap.settings import website_URL, discord_webhook_url

def GetSideContentData(request):
    if "notification" in request.POST:
        notification = Notification.objects.get(id=int(request.POST['notification']))
        direct_post = str(notification.link)
        notification.delete()
        HttpResponseRedirect(direct_post)
    if request.method == "post":
            if "todo" in request.POST:
                task = ToDo.objects.get(id=request.POST['todo'])
                task.is_finished = True
                task.save()

    topUsers = member.objects.filter(NumberOfPosts__gt=0).order_by('-NumberOfPosts')
    TopUsersForDisplay=[]
    cnt = 1
    for topUser in topUsers:
        TopUsersForDisplay.append(topUser)
        if cnt == 5:
            break
        cnt+=1

    data = {
        "Announcements": Announcement.objects.filter(id__gt=Announcement.objects.all().values().count()-10).order_by('-created_at'),
        "topUsers": TopUsersForDisplay,
    }
    data['info'] = [
        f"<b>{member.objects.all().count()}</b> tài khoản đã được tạo",
        f"<b>{Post.objects.filter(is_publish=True, is_verify=True).count()}</b> bài viết về học tập đã được tạo",
        f"<b>{Test.objects.filter(is_publish=True, is_verify=True).count()}</b> bài viết về kiểm tra đã được tạo"
    ]
    if request.user.is_authenticated:
        data["todo"] = ToDo.objects.filter(user=User.objects.get(username=request.user.username)).order_by("is_finished")
        data['notifications'] = Notification.objects.filter(user=User.objects.get(username=request.user.username)).order_by('-created_at','-id')

    return data

def get_website_info():
    user_count = len(member.objects.all())
    p_count = len(Post.objects.filter(is_publish=True)) + len(Test.objects.filter(is_publish=True))
    return {
        "user_count" : user_count,
        'p_count' : p_count,
    }

def getBadwords():
    return BadWord.objects.all() or {}
    # return {}

def markdown_to_html(content):
    #linebreak
    content = re.sub(r"\n", r"\n\n", content)
    content = markdown(content).replace('<img', "<img class='content-img'")
    content = content.replace('href', 'target="_blank" href')
    return content

#discord webhook
headers = {
    'Content-Type': 'application/json'
}

def embed_builder(title, desc, url):
	embed =	{
        "title": title,
        "description": f"Mô tả: {desc}",
        "url": url,
    }
	return embed

def discord_webhook(title, msg, mode, path):
    # payload = {
    #     "username": "CungNhauHocTap",
    #     "embeds": [embed_builder(f'CungNhauHocTap - {title}',
    #                               msg,
    #                               f'{website_URL}{path}')]
    # }
    # response = requests.post(discord_webhook_url[mode], data=json.dumps(payload), headers=headers)
    # if response.status_code == 204:
    #     return True
    # else:
    #     return False
    return True

def Discrd_Notification(discord_user, title, content, link):
    payload = {
        "username": "CungNhauHocTap - Thông báo",
        "content": f"<@{discord_user.id}> - Bạn nhận được thông báo.",
        "embeds": [embed_builder(f'CungNhauHocTap - Thông Báo',
                                  "Bạn vui lòng kiểm tra đường link bên dưới nhé.",
                                  f'{website_URL}/profile/notification')]
    }
    response = requests.post(discord_webhook_url['notification'], data=json.dumps(payload), headers=headers)
    if response.status_code == 204:
        return True
    else:
        return False

def createNotification(user_target, title, content, link):
    user = user_target

    Notification.objects.create(
        user=user,
        title=title,
        content = content,
        link=link,
    )
    return True

def own_post(request, baiviet):
    is_admin = member.objects.get(user=request.user).role == 'A'
    if (is_admin):
        return True
    else:
        return request.user == baiviet.author

def Like_Dislike_Process(request, model):
    baiviet = model
    if request.method == 'POST':
        baiviet = model
        if (request.user.is_authenticated):
            if not (request.user.username in baiviet.interactiveUsers):
                if request.POST['vote'] == "like":
                    baiviet.NumberOfLike += 1
                else:
                    baiviet.NumberOfDislike += 1
            else:
                if (request.POST['vote'] != baiviet.interactiveUsers.get(request.user.username)):
                    if request.POST['vote'] == "like":
                        baiviet.NumberOfLike += 1
                        baiviet.NumberOfDislike -= 1
                    else:
                        baiviet.NumberOfDislike += 1
                        baiviet.NumberOfLike -= 1
            baiviet.interactiveUsers.update({
                f"{request.user.username}": request.POST['vote']
            })
            baiviet.save()
    return baiviet