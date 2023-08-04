from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect

from .forms import PostForm, TestForm, TestFormInit
from .models import Post, Test, Tag, GroupTag
from .func import get_correct_answer_from_text, get_newest_posts, get_newest_tests, get_tag
from question.models import Question
from .func import save_post, changePost, save_test, changeTest
from Profile.models import Profile as member
from django.contrib.auth.models import User

import re
from Others.func import get_website_info, markdown_to_html, Like_Dislike_Process, createNotification, own_post
from Profile.models import Profile

def indexView(request):
    data = get_website_info()
    data['tieu_diem'] = request.GET.get('view_mode', 'tieu_diem') == 'tieu_diem'
    if (data['tieu_diem'] == True):
        data['posts'] = get_newest_posts(10)
        data['tests'] = get_newest_tests(10)
    else:
        data['posts'] = get_newest_posts(30)
        data['tests'] = get_newest_tests(30)
    return render(request, 'bai_viet/bai_viet.html', data)

# post
def hoctapView(request):
    data = get_website_info()
    paginator = {}
    data['is_tieu_diem'] = request.GET.get('view_mode', 'tieu_diem') == 'tieu_diem'
    data['sort_by'] = request.GET.get('sort_by', 'date_newest')
    data['view_mode'] = request.GET.get('view_mode', 'tieu_diem')

    PostList = Post.objects.filter(is_publish=True)
    if data['sort_by'] == 'date_newest':
        PostList = PostList.order_by('-createdAt')
    elif data['sort_by'] == 'date_oldest':
        PostList = PostList.order_by('createdAt')
    elif data['sort_by'] == 'likes_desc':
        PostList = PostList.order_by('-NumberOfLike')
    elif data['sort_by'] == 'likes_asc':
        PostList = PostList.order_by('NumberOfLike')

    if (data['is_tieu_diem']):
        paginator = Paginator(PostList, 15)
    else:
        paginator = Paginator(PostList, 30)
    try:
        page_number = request.GET['page']
    except:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    for post in page_obj:
        # post.content = markdown_to_html(post.content)
        words = post.content.split()
        if len(words) > 30:
            post.content = ' '.join(words[:30]) + '...'

    data['posts'] = page_obj
    return render(request, 'bai_viet/kien_thuc/home.html', data)
def searchPostView(request):
    data = get_website_info()
    data['is_searching'] = False

    if (request.method == 'GET') and ('title' in request.GET):
        if (request.GET['title'] == ''):
            data['is_searching'] = False
        else:
            data['posts'] = Post.objects.filter(title__icontains = request.GET['title'], is_verify=True, is_publish=True) | Post.objects.filter(post_id__contains = request.GET['title'], is_verify=True, is_publish=True)
            data['is_searching'] = True
            data['posts'] = data['posts'].order_by('-createdAt')

    return render(request, 'bai_viet/kien_thuc/search.html', data)
def PostDetailView(request, post_id):
    data = get_website_info()
    baiviet = Post.objects.get(post_id=post_id)
    baiviet = Like_Dislike_Process(request, baiviet)
    if (baiviet.is_publish == False) and (not own_post(request, baiviet)):
        return HttpResponseRedirect('/')

    last_voted = 'none'
    if request.user.username in baiviet.interactiveUsers:
        last_voted = str(baiviet.interactiveUsers.get(request.user.username))
    if (baiviet.is_publish) and (request.user.is_authenticated):
        baiviet.NumberOfSeen = baiviet.NumberOfSeen + 1
        baiviet.save()

    baiviet.content = markdown_to_html(baiviet.content)
    data.update({
        "post": baiviet,
        "own_post": request.user == baiviet.author,
        "interactiveUsersCount": int(baiviet.NumberOfLike) - int(baiviet.NumberOfDislike),
        "last_voted": last_voted,
    })
    return render(request, 'bai_viet/kien_thuc/detail.html', data)
@login_required(login_url='/login')
def createNewPostPageView(request):
    data = get_website_info()
    form = PostForm()
    tags_choice = get_tag()
    is_success = False
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            tagsChoosed = {}
            if ('tags' in request.POST):
                tagsChoosed = request.POST.getlist('tags')
            tags = {}
            for tag in tagsChoosed:
                tags[tag] = Tag.objects.get(id=tag).name
            is_success = save_post(form, request.user, tags)

    data["form"] = form
    data["is_success"] = is_success
    data["tags"] = tags_choice
    return render(request, 'bai_viet/kien_thuc/create.html', data)
    
@login_required(login_url='/login')
def PostChangeView(request, post_id):
    data = get_website_info()
    tags_choice = get_tag()
    post = Post.objects.get(post_id = post_id)
    if (post.is_verify == False) or (post.is_publish == False):
        return HttpResponseRedirect('/')
    if (not own_post(request, post)):
        return HttpResponseRedirect(f'/p/hoc_tap/p/{post.post_id}/')

    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if (form.is_valid()):
            tagsChoosed = {}
            if ('tags' in request.POST):
                tagsChoosed = request.POST.getlist('tags')
            tags = {}
            for tag in tagsChoosed:
                tags[tag] = Tag.objects.get(id=tag).name
            if (changePost(post, form, request.user, tags)):
                return HttpResponseRedirect(f'/p/hoc_tap/p/{post.post_id}/')
    form.fields['title'].initial = post.title
    form.fields['content'].initial = post.content
    data['form'] = form
    data['post'] = post
    data["tags"] = tags_choice
    return render(request, 'bai_viet/kien_thuc/change.html', data)
@login_required(login_url='/login')
def PostDeleteView(request, post_id):
    postDetail = Post.objects.get(post_id=post_id)
    if (request.user != postDetail.author):
        return HttpResponseRedirect(f'/p/hoc_tap/p/{postDetail.post_id}')
    postDetail.delete()
    return HttpResponseRedirect('/')

#test
def kiemtraView(request):
    data = get_website_info()
    paginator = {}
    data['is_tieu_diem'] = request.GET.get('view_mode', 'tieu_diem') == 'tieu_diem'
    data['sort_by'] = request.GET.get('sort_by', 'date_newest')
    data['view_mode'] = request.GET.get('view_mode', 'tieu_diem')

    PostList = get_newest_tests('all')
    if data['sort_by'] == 'date_newest':
        PostList = PostList.order_by('-createdAt')
    if data['sort_by'] == 'date_oldest':
        PostList = PostList.order_by('createdAt')

    if (data['is_tieu_diem']):
        paginator = Paginator(PostList, 15)
    else:
        paginator = Paginator(PostList, 30)
    try:
        page_number = request.GET['page']
    except:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    for post in page_obj:
        # post.content = markdown_to_html(post.content)
        words = post.content.split()
        if len(words) > 30:
            post.content = ' '.join(words[:30]) + '...'

    data['posts'] = page_obj
    return render(request, 'bai_viet/kiem_tra/home.html', data)
def searchTestView(request):
    data = get_website_info()
    data['is_searching'] = False

    if (request.method == 'GET') and ('title' in request.GET):
        data['is_searching'] = True
        data['tests'] = Test.objects.filter(title__icontains = request.GET['title'], is_verify=True, is_publish=True) | Test.objects.filter(test_id__contains = request.GET['title'], is_verify=True, is_publish=True)
       

    return render(request, 'bai_viet/kiem_tra/search.html', data)
@login_required(login_url='/login')
def TestDetailView(request, test_id):
    # xử lí làm bài kiểm tra
    data = get_website_info()
    data['is_finished'] = False
    baiviet = Test.objects.get(test_id=test_id)
    is_admin = Profile.objects.get(user=request.user).role == 'A'
    if (baiviet.is_publish == False) and (not is_admin) and (baiviet.author != request.user):
        return HttpResponseRedirect('/')
    data['own_post'] = (request.user.is_authenticated and (request.user == baiviet.author)) or (is_admin)

    if (request.method == 'POST'):
        if ('question1' in request.POST):
            data['is_finished'] = True

            correctAns = baiviet.correctAnswers
            UserAns = {}
            keys = request.POST.keys()
            for key in keys:
                if key.find('question') != -1:
                    UserAns[key] = request.POST[key]
            # Chấm Điểm
            correctCount = 0
            keys = baiviet.correctAnswers.keys()
            wrongAns = {}
            i = 1
            for key in keys:
                if correctAns[key] == UserAns[key]:
                    correctCount+=1
                else:
                    wrongAns[str(i)] = f'Câu hỏi <b>{i}</b>:\nĐáp án bạn chọn: <b>{UserAns[key]}</b>\nĐáp án đúng: <b>{correctAns[key]}</b>'
                i+=1

            #add user to data
            if not ( str(request.user.username) in baiviet.userJoined ):
                baiviet.userJoined[str(request.user.username)] = correctCount
                baiviet.save()
                data['message'] = f'Kết quả của bạn đã được lưu vào dữ liệu!'
            else:
                data['message'] = f'Kết quả của bạn không được lưu vào dữ liệu (Bạn đã làm bài thi này vào thời gian trước)!'

            data['correctCount'] = correctCount
            data['wrongAnswers'] = wrongAns.values()

    baiviet.content = markdown_to_html(baiviet.content)
    data['test'] = baiviet

    return render(request, 'bai_viet/kiem_tra/detail.html', data)
@login_required(login_url='/login')
def TestTopScoreView(request, test_id):
    data = get_website_info()
    baiviet = Test.objects.get(test_id=test_id)
    topscore = sorted(baiviet.userJoined.items(),reverse=True, key=lambda x:x[1])

    for i in range(len(topscore)):
        topscore[i] += tuple(f"{i+1}")

    paginator = Paginator(topscore, 30)
    try:
        page_number = request.GET['page']
    except:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    data['test'] = baiviet
    data['topScore'] = page_obj

    return render(request, 'bai_viet/kiem_tra/topscore.html', data)
@login_required(login_url='/login')
def createNewTestPageView(request):
    data = get_website_info()
    tags_choice = get_tag()
    form = TestFormInit()
    correct_ans = {}
    num_of_questions = 0

    data['is_success'] = False
    data['num_of_questions'] = request.POST.get('num_of_questions')
    data["tags"] = tags_choice
    data['message'] = None

    if request.method == 'POST':
        if ('number_questions' in request.POST):
            form = TestFormInit(request.POST)
            if form.is_valid():
                data['num_of_questions'] = form.cleaned_data['number_questions']
                #get question (optional)
                correct_ans = form.cleaned_data['correct_ans']
                if (correct_ans == None):
                    pass
                else:
                    correct_ans = get_correct_answer_from_text(correct_ans)
                    if (correct_ans != False):
                        data['correct_ans'] = correct_ans
                form = TestForm()
                num_of_questions = data['num_of_questions']
        else:
            # get right ans
            correct_ans = {}
            keys = request.POST.keys()
            for key in keys:
                if key.find('question') != -1:
                    correct_ans[key] = request.POST[key]
            form = TestForm(request.POST)
            if form.is_valid():
                data['is_success'] = True
                #tags
                tagsChoosed = {}
                if ('tags' in request.POST):
                    tagsChoosed = request.POST.getlist('tags')
                tags = {}
                for tag in tagsChoosed:
                    tags[tag] = Tag.objects.get(id=tag).name
                data['is_success'] = save_test(form, request.user, tags, correct_ans)
            else:
                form = TestForm()
                form.fields['title'].initial = request.POST.get('title')
                form.fields['content'].initial = request.POST.get('content')
                data['message'] = "Bài kiểm tra của bạn chứa từ ngữ không phù hợp."
                data['correct_ans'] = correct_ans
                data['num_of_questions'] = len(correct_ans)

    data["form"] = form
    temp = []
    for i in range(num_of_questions):
        temp.append(i+1)
    data['idListQuestion'] = temp
    print(correct_ans)

    return render(request, 'bai_viet/kiem_tra/create.html', data)
@login_required(login_url='/login')
def TestChangeView(request, test_id):
    data = get_website_info()
    test = Test.objects.get(test_id = test_id)
    form = TestForm()
    form.fields['title'].initial = test.title
    form.fields['content'].initial = test.content
    data['test'] = test

    if (test.is_publish == False):
        return HttpResponseRedirect(f'/p/kiem_tra/p/{test.test_id}')
    if (not own_post(request, test)):
        return HttpResponseRedirect(f'/p/kiem_tra/p/{test.test_id}')

    if (request.method == 'POST'):
        form = TestForm(request.POST)
        if form.is_valid():
            # get right ans
            correct_ans = {}
            keys = request.POST.keys()
            for key in keys:
                if key.find('question') != -1:
                    correct_ans[key] = request.POST[key]
            #tags
            tagsChoosed = {}
            if ('tags' in request.POST):
                tagsChoosed = request.POST.getlist('tags')
            tags = {}
            for tag in tagsChoosed:
                tags[tag] = Tag.objects.get(id=tag).name

            if (changeTest(test, form, request.user, tags, correct_ans)):
                return HttpResponseRedirect(f'/p/kiem_tra/p/{test.test_id}')

    data['form'] = form
    data['correct_ans'] = test.correctAnswers
    data["tags"] = get_tag()
    return render(request, 'bai_viet/kiem_tra/change.html', data)
@login_required(login_url='/login')
def TestDeleteView(request, test_id):
    postDetail = Test.objects.get(test_id=test_id)
    if (request.user != postDetail.author):
        return HttpResponseRedirect(f'/p/kiem_tra/p/{postDetail.test_id}')
    postDetail.delete()
    return HttpResponseRedirect('/')

def TagHomeView(request):
    data = get_website_info()
    data['groups'] = GroupTag.objects.all()
    data['tags'] = Tag.objects.all()
    return render(request, 'bai_viet/tag/home.html', data)

def TagDetailView(request, id):
    data = get_website_info()
    tag = Tag.objects.get(id=id)
    data['tag'] = tag
    data['posts'] = Post.objects.filter(is_publish=True, tags__has_keys=[tag.id])
    data['tests'] = Test.objects.filter(is_publish=True, tags__has_keys=[tag.id])
    return render(request, 'bai_viet/tag/detail.html', data)