from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('search', views.search),
    path('create', views.create),
    path('detail/<id>', views.detail),
    path('detail/<id>/change', views.change),
    path('detail/<id>/delete', views.delete),
    path('answer/<id>', views.answerDetail),
]