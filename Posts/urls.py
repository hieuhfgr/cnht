from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexView, name='home_p'),
    path('hoc_tap/', views.hoctapView),
    path('hoc_tap/search', views.searchPostView),
    path('hoc_tap/create', views.createNewPostPageView),
    path('hoc_tap/tag/', views.TagHomeView),
    path('hoc_tap/tag/<str:id>', views.TagDetailView),
    path('hoc_tap/p/<str:post_id>/', views.PostDetailView),
    path('hoc_tap/p/<str:post_id>/change', views.PostChangeView),
    path('hoc_tap/p/<str:post_id>/delete', views.PostDeleteView),

    path('kiem_tra/', views.kiemtraView),
    path('kiem_tra/search', views.searchTestView),
    path('kiem_tra/create', views.createNewTestPageView),
    path('kiem_tra/p/<str:test_id>/', views.TestDetailView),
    path('kiem_tra/p/<str:test_id>/topscore', views.TestTopScoreView),
    path('kiem_tra/p/<str:test_id>/change', views.TestChangeView),
    path('kiem_tra/p/<str:test_id>/delete', views.TestDeleteView),
    
]