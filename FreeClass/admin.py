from django.contrib import admin
from .models import FreeClassLink

class FreeClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'author', 'is_verify', 'link')
    search_fields = ['author']
    list_filter = ['is_verify']

admin.site.register(FreeClassLink, FreeClassAdmin)