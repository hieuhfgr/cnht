from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from .models import Question, Answer, MessageQnA
from .forms import Questionform, AnswerForm, MessageForm

import re
from Others.func import get_website_info, markdown_to_html, Like_Dislike_Process, discord_webhook, createNotification
from Profile.models import Profile
from Profile.func import autoPublish
from cungnhauhoctap.settings import website_URL


@login_required(login_url='/login')
def home(request):
    data = get_website_info()
    QuestionList = Question.objects.filter(is_published=True)
    paginator = {}
    data['sort_by'] = request.GET.get('sort_by', 'date_newest')

    if data['sort_by'] == 'date_newest':
        QuestionList = QuestionList.order_by('-createdAt')
    elif data['sort_by'] == 'date_oldest':
        QuestionList = QuestionList.order_by('createdAt')
    elif data['sort_by'] == 'open':
        QuestionList = QuestionList.filter(is_open = True)
    elif data['sort_by'] == 'close':
        QuestionList = QuestionList.filter(is_open = False)

    paginator = Paginator(QuestionList, 20)
    try:
        page_number = request.GET['page']
    except:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    data['questions'] = page_obj
    return render(request, 'question/home.html', data)

@login_required(login_url='/login')
def search(request):
    data = get_website_info()
    data['is_searching'] = False
    query = request.GET.get('q', None)
    if (query != '' and query != None):
        QuestionList = Question.objects.filter(is_published=True, title__icontains=query)
        data['is_searching'] = True
        data['questions'] = QuestionList
    return render(request, 'question/search.html', data)

@login_required(login_url='/login')
def detail(request, id):
    data = get_website_info()
    baiviet = Question.objects.get(id=id)
    answers = Answer.objects.filter(question=baiviet, isHide=False, is_visible=False).order_by('-NumberOfLike')
    baiviet.comment_count = len(answers)
    baiviet.save()
    form = AnswerForm()

    is_admin = Profile.objects.get(user=request.user).role == 'A'
    if (baiviet.is_published == False) and (not is_admin) and (baiviet.author != request.user):
        return HttpResponseRedirect('/')
    if ('vote' in request.POST):
        baiviet = Like_Dislike_Process(request, baiviet)
    if ('answer-vote' in request.POST):
        id, vote = request.POST.get('answer-vote').split('-')
        try:
            interactive_ans = Answer.objects.get(id=id)
            if not (request.user.username in interactive_ans.interactiveUsers):
                if vote == "like":
                    interactive_ans.NumberOfLike += 1
                else:
                    interactive_ans.NumberOfDislike += 1
            else:
                if (vote != interactive_ans.interactiveUsers.get(request.user.username)):
                    if vote == "like":
                        interactive_ans.NumberOfLike += 1
                        interactive_ans.NumberOfDislike -= 1
                    else:
                        interactive_ans.NumberOfDislike += 1
                        interactive_ans.NumberOfLike -= 1
            interactive_ans.interactiveUsers.update({
                f"{request.user.username}": vote
            })
            interactive_ans.save()
        except:
            pass
    last_voted = 'none'
    if request.user.username in baiviet.interactiveUsers:
        last_voted = str(baiviet.interactiveUsers.get(request.user.username))
    is_user_posted_answer = request.user in [ans.user for ans in answers]
    if ('content' in request.POST):
        form = AnswerForm(request.POST)
        if form.is_valid():
            if (is_user_posted_answer==False):
                createNotification( baiviet.author,
                                    f"Thông Báo Hỏi Đáp",
                                    f"{request.user.username} đã trả lời câu hỏi của bạn trong hỏi đáp {baiviet.title}",
                                    f"{website_URL}/question/detail/{baiviet.id}")
                Answer.objects.create(
                    question=baiviet,
                    user=request.user,
                    content=form.cleaned_data['content']
                )
            else:
                AnswerChange = Answer.objects.get(question=baiviet, user=request.user) 
                AnswerChange.content = form.cleaned_data['content']
                AnswerChange.save()
            is_user_posted_answer = True
            

    if ('answer_action' in request.POST):
        action = request.POST.get('answer_action')
        if (action == "change"):
            is_user_posted_answer = False
            form.fields['content'].initial = Answer.objects.get(question=baiviet, user=request.user).content
        elif (action == "delete"):
            ans = Answer.objects.get(question=baiviet, user=request.user)
            ans.delete()
            is_user_posted_answer = False

    if (('correct_answer' in request.POST)):
        if ((request.user == baiviet.author)):
            correct_ans = Answer.objects.get(id=request.POST.get('correct_answer'))
            correct_ans.is_correct = True
            correct_ans.save()
            baiviet.is_finished = True
            baiviet.is_open = False
            baiviet.save()

    answers = Answer.objects.filter(question=baiviet, isHide=False, is_visible=False).order_by('-is_correct', '-NumberOfLike')
    for ans in answers:
        ans.content = markdown_to_html(ans.content)
    baiviet.content = markdown_to_html(baiviet.content)

    data.update({
        'post': baiviet,
        'answers': answers,
        'has_correct_answer': len(Answer.objects.filter(question=baiviet, is_correct=True)) != 0,
        "own_post": request.user == baiviet.author,
        "interactiveUsersCount": int(baiviet.NumberOfLike) - int(baiviet.NumberOfDislike),
        "last_voted": last_voted,
        "answerForm": form,
        "is_user_posted_answer": is_user_posted_answer
    })
    
    return render(request, 'question/detail.html', data)

@login_required(login_url='/login')
def create(request):
    data = get_website_info()
    form = Questionform()
    data['is_success'] = False
    if (request.method == 'POST'):
        form = Questionform(request.POST)
        if form.is_valid():
            question = Question.objects.create(
                title = form.cleaned_data['title'],
                content = form.cleaned_data['content'],
                author = request.user,
            )
            if (autoPublish(request.user)):
                question.is_verified = True
                question.is_published = True
                question.save()
                return HttpResponseRedirect(f'/question/detail/{question.id}')
            else:
                data['is_success'] = discord_webhook("Duyệt Bài",
                            f"Link duyệt: {website_URL}/admin/question/question/{question.id}/change/ \nLink preview bài viết: {website_URL}/question/detail/{question.id}/", 
                            "private", f'/admin/question/question/{question.id}/change/')
    data['form'] = form
    return render(request, 'question/create.html', data)

@login_required(login_url='/login')
def change(request, id):
    data = get_website_info()
    question = Question.objects.get(id=id)
    is_admin = Profile.objects.get(user=request.user).role == 'A'
    if (not is_admin) and (question.author != request.user):
        return HttpResponseRedirect(f'/question/detail/{question.id}')

    form = Questionform()
    if ((request.method == 'POST') and ('title' in request.POST) and ('content' in request.POST)):
        form = Questionform(request.POST)
        if form.is_valid():
            question.title = form.cleaned_data['title']
            question.content = form.cleaned_data['content']
            if (not autoPublish(request.user)):
                question.is_published = False
                question.is_verified = False
                discord_webhook("Duyệt Bài",
                    f"Link duyệt: {website_URL}/admin/question/question/{question.id}/change/ \nLink preview bài viết: {website_URL}/question/detail/{question.id}/", 
                    "private", f'/admin/question/question/{question.id}/change/')
            else:
                question.is_published = True
                question.is_verified = True

            question.save()
            return HttpResponseRedirect(f'/question/detail/{question.id}')

    form.fields['title'].initial = question.title
    form.fields['content'].initial = question.content
    
    data.update({
        'form': form,
        'post': question
    })
    
    return render(request, 'question/change.html', data)

@login_required(login_url='/login')
def delete(request, id):
    question = Question.objects.get(id=id)
    if question.author == request.user:
        question.delete()
        return HttpResponseRedirect(f'/question/')
    else:
        return HttpResponseRedirect(f'/question/detail/{question.id}')

@login_required(login_url='/login')
def answerDetail(request, id):
    #id tuong trung cua ans
    data = get_website_info()
    ans = Answer.objects.get(id=id)
    baiviet = ans.question
    data['message'] = False

    is_admin = Profile.objects.get(user=request.user).role == 'A'
    if (baiviet.is_published == False) and (not is_admin) and (baiviet.author != request.user):
        return HttpResponseRedirect('/')

    ans.content = markdown_to_html(ans.content)
    baiviet.content = markdown_to_html(baiviet.content)
    if ('message' in request.POST):
        form = MessageForm(request.POST)
        if form.is_valid():
            MessageQnA.objects.create(
                answer=ans,
                user=request.user,
                content=form.cleaned_data['message']
            )
        else:
            form.fields['message'].initial = request.POST.get('message', '')
            data['message'] = 'Tin nhắn của bạn chứa từ ngữ không phù hợp' 
    
    messages = MessageQnA.objects.filter(answer=ans, isHide=False).order_by('createdAt')
    form = MessageForm()

    data['post'] = baiviet 
    data['ans'] = ans
    data['messages'] = messages
    data['form'] = form
    return render(request, 'question/answer/detail.html', data)