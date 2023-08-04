from django import forms
from .models import Question
#thu vien chuan hoa
from Others.func import getBadwords

class Questionform(forms.Form):
    title = forms.CharField(label="Tiêu đề câu hỏi", max_length=255)
    content = forms.CharField(label="Nội dung câu hỏi", widget=forms.Textarea ,min_length=10)

    def clean_title(self):
        badwords = getBadwords()
        title = (self.cleaned_data['title'].lower())
        for word in badwords:
            if title.find(word.word) != -1:
                raise forms.ValidationError('Tiêu đề của bạn chứa từ ngữ không phù hợp')
        return self.cleaned_data['title']

    def clean_content(self):
        badwords = getBadwords()
        content = (self.cleaned_data['content'].lower())
        for word in badwords:
            if content.find(word.word) != -1:
                raise forms.ValidationError('Nội dung của bạn chứa từ ngữ không phù hợp')
        return self.cleaned_data['content']

class AnswerForm(forms.Form):
    content = forms.CharField(label="Câu trả lời của bạn", widget=forms.Textarea(), min_length=3)

    def clean_content(self):
        badwords = getBadwords()
        content = (self.cleaned_data['content'].lower())
        for word in badwords:
            if (content.find(word.word) != -1):
                raise forms.ValidationError('Câu trả lời của bạn chứa từ ngữ không phù hợp')
        return self.cleaned_data['content']

class MessageForm(forms.Form):
    message = forms.CharField(min_length=1)

    def clean_message(self):
        badwords = getBadwords()
        message = (self.cleaned_data['message'].lower())
        for word in badwords:
            if (message.find(word.word) != -1):
                raise forms.ValidationError('Tin nhắn của bạn chứa từ ngữ không phù hợp')
        return self.cleaned_data['message']

