from django.contrib import admin
from .models import FaQ, AdminUser, Announcement, BadWord

class teamAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ['user']
    list_filter = ['role']

class announcementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ['author']
    list_filter = ['author']    

class faqAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

class BadWordAdmin(admin.ModelAdmin):
    list_display = ['word']
    search_fields = ['word']

admin.site.register(Announcement, announcementAdmin)
admin.site.register(AdminUser, teamAdmin)
admin.site.register(FaQ, faqAdmin)
admin.site.register(BadWord, BadWordAdmin)