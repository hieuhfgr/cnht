from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.views import serve
from login_register.views import registerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('p/', include('Posts.urls')),
    path('question/', include('question.urls')),
    path('profile/', include('Profile.urls')),
    path('todo/', include('Todo.urls')),
    path('free-class/', include('FreeClass.urls')),
    path('oauth2/', include('oauth2.urls')),

    path('auth/', include('login_register.urls')),
    path('login/', auth_views.LoginView.as_view(next_page='/'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', registerView, name='register'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)