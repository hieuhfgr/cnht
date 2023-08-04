from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from cungnhauhoctap.settings import EMAIL_HOST_USER
from login_register.func import send_email_verification
from login_register.forms import RegisterForm

User = get_user_model()

def registerView(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login/")
    return render(request, 'registration/register.html', {
        'form': form,
    })


def send_verification_email(request):
    if 'email_verification' in request.session:
        email = request.session['email_verification']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Tài khoản không tồn tại')
            return render(request, 'verification/send_email.html')
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        verify_url = request.build_absolute_uri(
            f'/auth/verify-email/{uidb64}/{token}/'
        )
        if (send_email_verification(email, verify_url)):
            messages.success(request, 'Đã gửi email xác thực')
            return redirect('send_verification_email')
        else:
            messages.error(request, 'Đã có lỗi xảy ra')
    return render(request, 'verification/send_email.html')

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Email của bạn đã được xác thực thành công!')
        del request.session['email_verification']
        return redirect('/')
    else:
        messages.error(request, 'Đường dẫn xác thực không hợp lệ hoặc đã hết hạn')
        return redirect('send_verification_email')