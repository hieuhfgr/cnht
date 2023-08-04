from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import ToDo, ToDo_GroupUser
from .func import finish_task, delSpace, can_access_todo_group, finish_task_group
from Others.func import get_website_info
from Profile.func import is_own_page

@login_required(login_url='/login')
def TodoListView(request):
    data = get_website_info()

    if request.method == 'POST':
        id = request.POST['taskFinish']
        if 'taskFinish' in request.POST.dict():
            finish_task(request, id)

    todo = ToDo.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(todo, 30)
    try:
        page_number = request.GET['page']
    except:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    data['todo'] = page_obj

    return render(request, 'todo/home.html', data)

@login_required(login_url='/login')
def TodoCreateView(request):
    data = get_website_info()
    if request.method == 'POST':
        newTodo = ToDo.objects.create(
            user=User.objects.get(username=str(request.user.username)),
            title=request.POST['taskTitle'],
            detail=request.POST['taskDetail'],
        )
        return HttpResponseRedirect(f'/todo/detail/{newTodo.id}')
    return render(request, 'todo/create.html', data)

@login_required(login_url='/login')
def TodoTaskDetailView(request, id):
    data = get_website_info()
    task = ToDo.objects.get(id=id)

    if (not is_own_page(request, task.user)):
        return HttpResponseRedirect('/todo/')

    if (request.method == 'POST'):
        finish_task(request, id)
    task = ToDo.objects.get(id=id)
    data['task'] = task
    return render(request, 'todo/detail.html', data)

@login_required(login_url='/login')
def TodoChangeView(request, id):
    data = get_website_info()
    task = ToDo.objects.get(id=id)
    if (not is_own_page(request, task.user)):
        return HttpResponseRedirect('/todo/')
    if request.method == 'POST':
        if 'is_finished' in request.POST.dict():
            if request.POST['is_finished'] == 'false':
                task.is_finished = False
            elif request.POST['is_finished'] == 'true':
                task.is_finished = True
            task.save()
            return HttpResponseRedirect(f'/todo/detail/{task.id}')

        if 'taskTitle' in request.POST.dict():
            taskTitle = request.POST['taskTitle']
            taskDetail = request.POST['taskDetail']
            if taskTitle.count(" ") != len(taskTitle):
                task.title = taskTitle
            task.detail = taskDetail
            task.save()
            return HttpResponseRedirect(f'/todo/detail/{task.id}')

    data['task'] = ToDo.objects.get(id=id)
    return render(request, 'todo/change.html', data)

@login_required(login_url='/login')
def TodoDeleteView(request, id):
    data = get_website_info()
    task = ToDo.objects.get(id=id)
    if (not is_own_page(request, task.user)):
        return HttpResponseRedirect('/todo/')

    if (request.method == 'POST'):
        task.delete()
        return HttpResponseRedirect('/todo')
    data['task'] = task
    return render(request, 'todo/delete.html', data)


# --group--
@login_required(login_url='/login')
def GroupTodoListView(request):
    data = get_website_info()
    todos_owned = ToDo_GroupUser.objects.filter(user=request.user).order_by('is_finished')
    todos_add = ToDo_GroupUser.objects.filter(access_user__has_key=request.user.username).order_by('is_finished')
    paginator_owned = Paginator(todos_owned, 20)
    paginator_add = Paginator(todos_add, 20)

    page_number_owned = request.GET.get('page_owned', 1)
    page_number_add = request.GET.get('page_add', 1)

    todos_owned_page = paginator_owned.get_page(page_number_owned)
    todos_add_page = paginator_add.get_page(page_number_add)

    data['todos_owned'] = todos_owned_page
    data['todos_add'] = todos_add_page

    return render(request, 'todo/group/home.html', data)

@login_required(login_url='/login')
def GroupTodoCreateView(request):
    data = get_website_info()
    if request.method == 'POST':
        if (request.POST['users'] != ""):
            users = request.POST['users'].split(',')
            users = delSpace(users)
            access_user = {}
            error = ""
            for user in users:
                if (user == str(request.user.username)):
                    continue
                check = User.objects.filter(username=user)
                if(len(check) == 0):
                    error=f'Tên người dùng "{user}" không có trong dữ liệu!'
                    break
                else:
                    access_user[user] = check[0].first_name
            if (error == ""):
                newTodo = ToDo_GroupUser.objects.create(
                    user=User.objects.get(username=str(request.user.username)),
                    title=request.POST['taskTitle'],
                    detail=request.POST['taskDetail'],
                    access_user=access_user
                )
                return HttpResponseRedirect(f'/todo/g/detail/{newTodo.id}')
            else:
                data['error'] = error
        else:
            data['error'] = "Bạn chưa điền vào ô <b>Người dùng truy cập công việc!</b>"
    return render(request, 'todo/group/create.html', data)

@login_required(login_url='/login')
def GroupTodoDetailView(request, id):
    data = get_website_info()
    data['task'] = ToDo_GroupUser.objects.get(id=id)

    if (not can_access_todo_group(request, data['task'])):
        return HttpResponseRedirect('/todo/g')
    if (request.method == 'POST') and (data['task'].user == request.user):
        finish_task_group(request, id)
    data['task'] = ToDo_GroupUser.objects.get(id=id)
    return render(request, 'todo/group/detail.html', data)

@login_required(login_url='/login')
def GroupTodoChangeView(request, id):
    data = get_website_info()
    task = ToDo_GroupUser.objects.get(id=id)
    if (not is_own_page(request, task.user)):
        return HttpResponseRedirect('/todo/g/')
    if request.method == 'POST':
        if 'is_finished' in request.POST.dict():
            if request.POST['is_finished'] == 'false':
                task.is_finished = False
            elif request.POST['is_finished'] == 'true':
                task.is_finished = True
            task.save()
            return HttpResponseRedirect(f'/todo/g/detail/{task.id}')

        if 'taskTitle' in request.POST.dict():
            taskTitle = request.POST['taskTitle']
            taskDetail = request.POST['taskDetail']
            if taskTitle.count(" ") != len(taskTitle):
                task.title = taskTitle
            task.detail = taskDetail
            task.save()
            return HttpResponseRedirect(f'/todo/g/detail/{task.id}')
    data['task'] = ToDo_GroupUser.objects.get(id=id)
    return render(request, 'todo/group/change.html', data)

@login_required(login_url='/login')
def GroupTodoDeleteView(request, id):
    data = get_website_info()
    task = ToDo_GroupUser.objects.get(id=id)
    if (not is_own_page(request, task.user)):
        return HttpResponseRedirect('/todo/g/')
    if (request.method == 'POST'):
        task.delete()
        return HttpResponseRedirect('/todo/g')
    data['task'] = task
    return render(request, 'todo/group/delete.html', data)
