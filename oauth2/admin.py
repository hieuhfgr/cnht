from django.contrib import admin
from .models import DiscordUser

class DiscordUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'createdAt', 'last_login')
    search_fields=['id']

admin.site.register(DiscordUser, DiscordUserAdmin)