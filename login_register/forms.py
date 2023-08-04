from django import forms
import re
from django.core.exceptions import ObjectDoesNotExist

from Profile.models import Profile as profile
from django.contrib.auth.models import User as user
from Others.func import getBadwords

class RegisterForm(forms.Form):
    username = forms.CharField(label='Tên Đăng Nhập (username)', max_length=30)
    firstname = forms.CharField(label='Tên', max_length = 30)
    lastname = forms.CharField(label='Họ', max_length = 50)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Mật Khẩu (password)', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Nhập Lại Mật Khẩu', widget=forms.PasswordInput)


    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if len(password1) < 8:
                raise forms.ValidationError('Mật khẩu của bạn quá ngắn. Độ dài của mật khẩu phải >= 8 kí tự')
            if password1 == password2 and password1:
                return password2
        raise forms.ValidationError('Mật khẩu không hợp lệ')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            temp = username.encode(encoding='ascii')
        except:
            raise forms.ValidationError("Tên tài khoản chứa kí tự không nằm trong bảng chữ cái tiếng Anh")

        if not (re.search(r'^\w+$', username)):
            raise forms.ValidationError("Tên tài khoản có kí tự đặc biệt")
        if (username == 'AnonymousUser'):
            raise forms.ValidationError("Tên tài khoản không hợp lệ")
        try:
            user.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError("Tài khoản đã tồn tại")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError("Email đã được đăng kí")

    def clean_firstname(self):
        bad_words = getBadwords()
        first_name = self.cleaned_data['firstname'].upper()
        first_name = first_name.replace('  ', ' ')
        for word in bad_words:
            if first_name.find(str(word).upper()) != -1:
                raise forms.ValidationError("Tên của bạn chứa từ ngữ không phù hợp")

        if not (re.search(r'^[AÁÀẢÃẠaáàảãạĂẮẰẲẴẶăắằẳẵạÂẤẦẨẪẬâấầẩẫậBbCcDdĐđEÉÈẺẼẸeéèẽẻẹÊẾỀỂỄỆêếềểễệGgHhIÍÌỈĨỊiíìỉĩịKkLlMmNnOÓÒỎÕỌoóòỏõọÔỐỒỔÕỌoóòỏõọƠỚỜỞỠỢơớờởỡợPpQqRrSsTtUÚỦŨỤuúùủũụƯỨỪỬỮỰưứừửữựVvXxYyZz ]+$', first_name)):
            raise forms.ValidationError("Tên của bạn không thể chứa các kí tự ngoài chữ hoa và chữ thường")
        if first_name.isspace() or first_name == '':
            raise forms.ValidationError("Tên của bạn không hợp lệ!")
        return self.cleaned_data['firstname']

    def clean_lastname(self):
        bad_words = getBadwords()
        last_name = self.cleaned_data['lastname'].upper()
        last_name = last_name.replace('  ', ' ')
        for word in bad_words:
            if last_name.find(str(word).upper()) != -1:
                raise forms.ValidationError("Họ của bạn chứa từ ngữ không phù hợp")
        if not (re.search(r'^[AÁÀẢÃẠaáàảãạĂẮẰẲẴẶăắằẳẵạÂẤẦẨẪẬâấầẩẫậBbCcDdĐđEÉÈẺẼẸeéèẽẻẹÊẾỀỂỄỆêếềểễệGgHhIÍÌỈĨỊiíìỉĩịKkLlMmNnOÓÒỎÕỌoóòỏõọÔỐỒỔÕỌoóòỏõọƠỚỜỞỠỢơớờởỡợPpQqRrSsTtUÚỦŨỤuúùủũụƯỨỪỬỮỰưứừửữựVvXxYyZz ]+$', last_name)):
            raise forms.ValidationError("Họ của bạn không thể chứa các kí tự ngoài chữ hoa và chữ thường")
        if last_name == '':
            raise forms.ValidationError("Họ của bạn không hợp lệ!")
        return self.cleaned_data['lastname']

    def save(self):
        user.objects.create_user(
            username = self.cleaned_data['username'],
            email = self.cleaned_data['email'],
            password = self.cleaned_data['password1'],
            first_name = self.cleaned_data['firstname'],
            last_name = self.cleaned_data['lastname'],
        )
        user_created = user.objects.get(username=self.cleaned_data['username'])
        profile.objects.create(
            user = user_created,
            name = user_created.last_name + " " + user_created.first_name,
        )