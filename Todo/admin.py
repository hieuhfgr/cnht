from django.contrib import admin
from .models import ToDo, ToDo_GroupUser

class ToDoAdmin(admin.ModelAdmin):
    list_display = ('title', "is_finished")
    search_fields = ['user']

admin.site.register(ToDo, ToDoAdmin)
admin.site.register(ToDo_GroupUser, ToDoAdmin)