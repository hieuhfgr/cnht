from django import forms
import re
from django.contrib.auth.models import User as user
from Others.func import getBadwords
bad_words = getBadwords()

class ChangeProfileForm(forms.Form):
    firstname = forms.CharField(label='Tên', max_length = 30)
    lastname = forms.CharField(label='Họ', max_length = 50)
    about = forms.CharField(label="About", widget=forms.Textarea)

    def clean_firstname(self):
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

    def clean_about(self):
        about = self.cleaned_data['about'].lower()
        for word in bad_words:
            if about.find(str(word)) != -1:
                raise forms.ValidationError("About của bạn chứa từ ngữ không phù hợp")
        return self.cleaned_data['about']