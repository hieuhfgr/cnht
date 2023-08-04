from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    about = models.TextField(default='người dùng không chia sẻ thông tin')
    roles = [
        ('S', 'Học sinh'),
        ('T', 'Giáo viên'),
        ('A', 'admin')
    ]
    ranks = [
        ('A', 'Vàng'),
        ('B', 'Bạc'),
        ('C', 'Đồng'),
        ('U', 'Chưa xếp hạng'),
    ]
    role = models.CharField(max_length=1 ,choices=roles, default='S')
    rank = models.CharField(max_length=1 ,choices=ranks, default='U')
    NumberOfPosts = models.IntegerField(default=0)
    NumberOfGoodPosts = models.IntegerField(default=0, help_text='tăng giá trị nếu bài viết của người dùng là tự viết')
    points = models.IntegerField(default=0, help_text='Điểm | dựa trên số bài viết đã đăng')
    chatGPTLimit = models.IntegerField(default=0, help_text='Giới hạn sử dụng ChatGPT API')
    createdAt = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    link = models.CharField(blank=True, max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)