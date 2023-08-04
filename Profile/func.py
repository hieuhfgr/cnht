from django.contrib.auth.models import User
from .models import Profile as profile
from Posts.models import Post, Test

def is_own_page(request, user):
    if request.user != user:
        return False
    else:
        return True

def update_top_users():
    allUser = User.objects.all()
    for user in allUser:
        posts_cnt= Post.objects.filter(is_publish=True, author=user).values().count()
        tests_cnt = Test.objects.filter(is_publish=True, author=user).values().count()
        good_posts_cnt= Post.objects.filter(is_publish=True, author=user, is_good_post = True).values().count()
        good_tests_cnt = Test.objects.filter(is_publish=True, author=user, is_good_test = True).values().count()

        user.NumberOfPosts = posts_cnt + tests_cnt
        user.NumberOfGoodPosts = good_posts_cnt + good_tests_cnt
        user.points = user.NumberOfGoodPosts * 2 + (user.NumberOfPosts - user.NumberOfGoodPosts)
        user.save()

def autoPublish(user):
    user = profile.objects.get(user=user)
    if (user.NumberOfGoodPosts >= 10) or (user.role == 'A'):
        return True
    else:
        return False