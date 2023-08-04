from django.shortcuts import render
from .models import FreeClassLink
from Others.func import markdown_to_html, get_website_info
from django.core.paginator import Paginator

def home(request):
    data = get_website_info()
    data['list'] = FreeClassLink.objects.filter(is_verify=True).order_by("-createdAt")
    paginator = Paginator(data['list'], 30)
    try:
        page_number = request.GET['page']
    except:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    data['list'] = page_obj
    return render(request, 'freeclass/home.html', data)

def detail(request, id):
    data = get_website_info()
    class_info = FreeClassLink.objects.get(id=id)
    class_info.description = markdown_to_html(class_info.description)
    data['class'] = class_info
    return render(request, 'freeclass/detail.html', data)