from django.contrib import admin
from .models import Post, Test, GroupTag, Tag

class TagInline(admin.TabularInline):
    model = Tag

class postAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'title', 'author', 'is_verify', 'is_publish')
    search_fields = ['post_id']
    list_filter = ['is_verify']

class testAdmin(admin.ModelAdmin):
    list_display = ('test_id', 'title', 'author', 'is_verify', 'is_publish')
    search_fields = ['test_id']
    list_filter = ['is_verify']

class GroupTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'createdAt')
    search_fields = ['id']
    inlines = [TagInline]

admin.site.register(Post, postAdmin)
admin.site.register(Test, testAdmin)
admin.site.register(GroupTag, GroupTagAdmin)