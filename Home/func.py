from Others.func import markdown_to_html
from .models import Announcement

def get_newest_announcement():
    tests = Announcement.objects.all().order_by('-created_at')
    return tests
