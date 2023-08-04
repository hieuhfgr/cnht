from django.db import models
from django.contrib.auth.models import User

class FaQ(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    def __str__(self):
        return self.title

AdminRoles = [
    ('A', 'quản lí'), #HA = Head Admin
    ('B', 'kiểm duyệt viên'), #KD = Kiểm Duyệt
    ('C', 'giúp đỡ'), # HP = Hepler
]

class AdminUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(choices=AdminRoles, max_length=2, help_text='vai trò của người quản lí')
    description = models.TextField(blank=True, help_text='mô tả | bạn lưu ý phải xóa hết text trong field rồi ghi mô tả của bạn nhé', default='không có mô tả về admin này!')
    avatar = models.ImageField(blank=True, upload_to='images', null=False, default='images/default.png', help_text='Lưu ý khi upload file ảnh: ảnh tỉ lệ 1:1 (hình vuông) và phải để tên file là họ và tên của bạn + năm sinh | ví dụ: nguyenminhhieu08')

    def __str__(self):
        return f"{self.user}, {self.role}"

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return f"{self.title} {self.author} {self.created_at}"

class BadWord(models.Model):
    word = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return f"{self.word}"
    
class ChangeLog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.created_at}] {self.title}"