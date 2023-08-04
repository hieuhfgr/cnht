from django.urls import path
from . import views

urlpatterns = [
    path('', views.TodoListView),
    path('create', views.TodoCreateView),
    #group todo

    path('g/', views.GroupTodoListView),
    path('g/create', views.GroupTodoCreateView),
    path('g/detail/<str:id>/', views.GroupTodoDetailView),
    path('g/detail/<str:id>/change', views.GroupTodoChangeView),
    path('g/detail/<str:id>/delete', views.GroupTodoDeleteView),

    path('detail/<str:id>/', views.TodoTaskDetailView),
    path('detail/<str:id>/change', views.TodoChangeView),
    path('detail/<str:id>/delete', views.TodoDeleteView),
]