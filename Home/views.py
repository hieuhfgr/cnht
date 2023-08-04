from django.shortcuts import render
from django.core.paginator import Paginator

from django.contrib.auth.models import User
from .models import Announcement, AdminUser, FaQ
from Profile.models import Profile
from question.models import Question

from Others.func import get_website_info
from Posts.func import get_newest_posts, get_newest_tests
from .func import get_newest_announcement
from Others.func import markdown_to_html

def home(request):
    data = get_website_info()
    if request.user.is_authenticated:
        data['user'] = User.objects.get(username = request.user.username)
    data['posts'] = get_newest_posts(10)
    data['tests'] = get_newest_tests(10)
    data['questions'] = Question.objects.filter(is_published=True, is_open=True).order_by('-createdAt')[:5]
    data['tieu_diem'] = request.GET.get('view_mode', 'tieu_diem') == 'tieu_diem'
    return render(request, 'home/home.html', data)


def about(request):
    data = get_website_info()
    return render(request, 'home/about.html', data)

def announcement(request):
    data = get_website_info()
    Announcement_list = get_newest_announcement()
    paginator = Paginator(Announcement_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data['announcements'] = page_obj
    return render(request, 'home/announcement/announcements.html',data)

def announcementDetail(request, id):
    data = get_website_info()
    announcement = Announcement.objects.get(id=id)
    announcement.content = markdown_to_html(announcement.content)
    data ['announcement'] = announcement
    return render(request, 'home/announcement/announcement.html', data)

def team(request):
    data = get_website_info()
    data['AdminUsers'] = AdminUser.objects.all().order_by('role')
    return render(request, 'home/team.html', data)

def faq(request):
    data = get_website_info()
    faqs = FaQ.objects.all()
    for faq in faqs:
        faq.content = markdown_to_html(faq.content)
    data['faqs'] = faqs
    return render(request, 'home/faqs.html', data)

def support(request):
    data = get_website_info()
    return render(request, 'home/support.html', data)