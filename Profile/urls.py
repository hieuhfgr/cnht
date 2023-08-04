from django.urls import path
from . import views

urlpatterns = [
    path('detail/<username>/', views.profileView),
    path('change', views.profileChangeView),
    path('claimrank', views.claimRankView),
    
    path('notification', views.profileNotification),
    path('notification/delete', views.profileNotificationDelete),
    path('my', views.redirectProfileView),
    path('search/', views.searchView),
    path('topusers/', views.topUserListView),
    path('setting', views.setting),
]