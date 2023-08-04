from .models import ToDo, ToDo_GroupUser

def finish_task(request, id):
    task = ToDo.objects.get(id = id)
    if (task.user == request.user):
        task.is_finished = True
        task.save()

def finish_task_group(request, id):
    task = ToDo_GroupUser.objects.get(id=id)
    if(task.user == request.user):
        task.is_finished = True
        task.save()

def delSpace(users):
    newusers = []
    for user in users:
        newusers.append(user.strip())
    return newusers

def can_access_todo_group(request, todo):
    username = str(request.user.username)
    access_user  = todo.access_user
    if (username in access_user.keys()) or (request.user == todo.user):
        return True
    else:
        return False

