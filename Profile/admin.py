from django.contrib import admin
from .models import Profile, Notification

class profileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'role', 'createdAt')
    search_fields=['user']
    list_filter = ('role', 'createdAt')

class notificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'createdAt')
    search_fields=['user']
    list_filter = ['createdAt']

admin.site.register(Profile, profileAdmin)
admin.site.register(Notification, notificationAdmin)