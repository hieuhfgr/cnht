import requests
import json
from django.core.mail import send_mail
from cungnhauhoctap.settings import EMAIL_HOST_USER

def send_email_verification(email, verify_url):
    subject = 'CungNhauHocTap - Xác thực email'
    message = f'Nhấp vào đường link sau để xác thực email của bạn: {verify_url}'
    from_email = 'cungnhauhoctap@outlook.com'
    recipient_list = [email]
    try:
        send_mail(subject, message, from_email, recipient_list)
        return True
    except Exception as e:
        print(e)
        return False