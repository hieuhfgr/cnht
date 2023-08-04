from django.urls import path
from .views import send_verification_email, verify_email

urlpatterns = [
    # path('send-verification-email/', send_verification_email, name='send_verification_email'),
    # path('verify-email/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),
]
