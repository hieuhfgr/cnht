from django.contrib import admin
from .models import Question, Answer, MessageQnA

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_verified', 'is_published','is_open', 'is_finished')
    search_fields = ['author']
    list_filter = ['is_verified']

class AnswerInline(admin.TabularInline):
    model = Answer

class ChatQnAInline(admin.TabularInline):
    model = MessageQnA

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'is_correct')
    search_fields = ['user']
    list_filter = ['is_correct']
    inlines = [ChatQnAInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)