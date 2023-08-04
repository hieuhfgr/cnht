from django import forms
from .models import Post, Tag
#thu vien chuan hoa
from Others.func import getBadwords


#post
class PostForm(forms.Form):
    title = forms.CharField(label="Tiêu đề bài viết", max_length=255)
    content = forms.CharField(label="Nội dung bài viết", widget=forms.Textarea ,min_length=10)

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

# class ChangePostForm(forms.Form):
#     title = forms.CharField(label="Tiêu đề bài viết", max_length=255)
#     content = forms.CharField(label="Nội dung bài viết", widget=forms.Textarea ,min_length=10)

#     def clean_title(self):
#         badwords = getBadwords()
#         title = self.cleaned_data['title'].lower()
#         for word in badwords:
#             if title.find(word.word) != -1:
#                 raise forms.ValidationError('Tiêu đề của bạn chứa từ ngữ không phù hợp')
#         return self.cleaned_data['title']

#     def clean_content(self):
#         badwords = getBadwords()
#         content = self.cleaned_data['content'].lower()
#         for word in badwords:
#             if content.find(word.word) != -1:
#                 raise forms.ValidationError('Nội dung của bạn chứa từ ngữ không phù hợp')
#         return self.cleaned_data['content']

class SendMessageForm(forms.Form):
    message = forms.CharField(label='Nhập tin nhắn:')

    def clean_message(self):
        badwords = getBadwords()
        message = self.cleaned_data['message'].lower()
        for word in badwords:
            if message.find(word.word) != -1:
                raise forms.ValidationError('tin nhắn của bạn chứa từ ngữ không phù hợp')

        return self.cleaned_data['message']

#test

class TestFormInit(forms.Form):
    number_questions = forms.IntegerField(label="Số câu hỏi", max_value=100, min_value=1)
    correct_ans = forms.CharField(label="Đáp Án (không bắt buộc nhập)", widget=forms.Textarea ,min_length=2, required=False, empty_value=None)


class TestForm(forms.Form):
    title = forms.CharField(label="Tiêu đề Kiểm Tra", max_length=255)
    content = forms.CharField(label="Nội dung Kiểm Tra", widget=forms.Textarea ,min_length=10)

    def clean_title(self):
        badwords = getBadwords()
        title = self.cleaned_data['title'].lower()
        for word in badwords:
            if title.find(word.word) != -1:
                raise forms.ValidationError('Tiêu đề của bạn chứa từ ngữ không phù hợp')
        return self.cleaned_data['title']
    def clean_content(self):
        badwords = getBadwords()
        content = self.cleaned_data['content'].lower()
        for word in badwords:
            if content.find(word.word) != -1:
                raise forms.ValidationError('Nội dung của bạn chứa từ ngữ không phù hợp')
        return self.cleaned_data['content']


# class ChangeTestForm(forms.Form):
#     title = forms.CharField(label="Tiêu đề Kiểm Tra", max_length=255)
#     content = forms.CharField(label="Nội dung Kiểm Tra", widget=forms.Textarea ,min_length=10)

#     def clean_title(self):
#         badwords = getBadwords()
#         title = self.cleaned_data['title'].lower()
#         for word in badwords:
#             if title.find(word.word) != -1:
#                 raise forms.ValidationError('Tiêu đề của bạn chứa từ ngữ không phù hợp')
#         return self.cleaned_data['title']
#     def clean_content(self):
#         badwords = getBadwords()
#         content = self.cleaned_data['content'].lower()
#         for word in badwords:
#             if content.find(word.word) != -1:
#                 raise forms.ValidationError('Nội dung của bạn chứa từ ngữ không phù hợp')
#         return self.cleaned_data['content']