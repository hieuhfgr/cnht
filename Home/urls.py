from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('about/', views.about),
    path('announcement/', views.announcement),
    path('announcement/<str:id>', views.announcementDetail),
    path('about/team/', views.team),
    path('about/faq/', views.faq),
    path('about/support/', views.support),
]