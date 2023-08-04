from .models import Post, Test, Tag
from Others.func import markdown_to_html, discord_webhook
from cungnhauhoctap.settings import website_URL
import re
from Profile.models import Profile
from Profile.func import autoPublish
from unidecode import unidecode


def get_newest_posts(count):
    posts = {}
    if (count == 'all'):
        posts = Post.objects.filter(is_publish=True).order_by('-createdAt')
    else:
        posts = Post.objects.filter(is_publish=True).order_by('-createdAt')[:count]
    for post in posts:
        # post.content = markdown_to_html(post.content)
        words = post.content.split()
        if len(words) > 30:
            post.content = ' '.join(words[:30]) + '...'
    return posts
def get_newest_tests(count):
    tests = {}
    if (count == 'all'):
        tests = Test.objects.filter(is_publish=True).order_by('-createdAt')
    else:
        tests = Test.objects.filter(is_publish=True).order_by('-createdAt')[:count]
    for test in tests:
        # test.content = markdown_to_html(test.content)
        words = test.content.split()
        if len(words) > 30:
            test.content = ' '.join(words[:30]) + '...'
    return tests
def create_post_id(title, p):
    if (p == 'post'):
        post_id = title + '_' + str(Post.objects.all().count() + 1)
    elif (p == 'test'):
        post_id = title + '_' + str(Test.objects.all().count() + 1)
    post_id = post_id.replace('  ',' ').replace(' ', '_').lower()
    post_id = re.sub(r'\W', '', post_id)
    return unidecode(post_id)

def get_tag():
    tags = Tag.objects.all()
    arr = []
    for tag in tags:
        arr.append((tag.id, tag.name))
    return arr

def save_post(form, user, tags):
    #auto save if user.role == 'giao vien' or has 10+ good posts
    profile = Profile.objects.get(user=user)
    if (profile.rank == 'A') or (profile.rank == 'T') or (autoPublish(user)):
        Post.objects.create(
            post_id = create_post_id(form.cleaned_data['title'], 'post'),
            title = form.cleaned_data['title'],
            content = form.cleaned_data['content'],
            author = user,
            is_verify = True,
            is_publish = True,
            tags = tags
        )
    else:
        post = Post.objects.create(
            post_id = create_post_id(form.cleaned_data['title'], 'post'),
            title = form.cleaned_data['title'],
            content = form.cleaned_data['content'],
            author = user,
            tags = tags
        )
        discord_webhook("Duyệt Bài",
                        f"Link duyệt: {website_URL}/admin/Posts/post/{post.id}/change/ \nLink preview bài viết: {website_URL}/p/hoc_tap/p/{post.post_id}/",
                        "private", f'/admin/Posts/post/{post.id}/change/')
    return True

def save_test(form, user, tags, correct_ans):
    #auto save if user.role == 'giao vien' or has 10+ good posts
    profile = Profile.objects.get(user=user)
    if (profile.rank == 'A') or (profile.rank == 'T') or (autoPublish(user)):
        Test.objects.create(
            test_id = create_post_id(form.cleaned_data['title'], 'test'),
            title = form.cleaned_data['title'],
            content = form.cleaned_data['content'],
            author = user,
            NumberOfQuestions = len(correct_ans),
            is_verify = True,
            is_publish = True,
            tags = tags,
            correctAnswers = correct_ans
        )
    else:
        post = Test.objects.create(
            test_id = create_post_id(form.cleaned_data['title'], 'test'),
            title = form.cleaned_data['title'],
            content = form.cleaned_data['content'],
            author = user,
            NumberOfQuestions = len(correct_ans),
            tags = tags,
            correctAnswers = correct_ans
        )
        discord_webhook("Duyệt Bài",
                        f"Link duyệt: {website_URL}/admin/Posts/test/{post.id}/change/ \nLink preview bài viết: {website_URL}/p/kiem_tra/p/{post.test_id}/",
                        "private", f'/admin/Posts/post/{post.id}/change/')
    return True

def changePost(post, form, user, tags):
    try:
        profile = Profile.objects.get(user=user)
        post.title = form.cleaned_data['title']
        post.content = form.cleaned_data['content']
        post.is_good_post = False
        post.tags = tags
        if not ((profile.rank == 'A') or (profile.rank == 'T') or (autoPublish(user))):
            post.is_verify = False
            post.is_publish = False
            discord_webhook("Duyệt Bài",
                        f"Link duyệt: {website_URL}/admin/Posts/post/{post.id}/change/ \nLink preview bài viết: {website_URL}/p/hoc_tap/p/{post.post_id}/",
                        "private", f'/admin/Posts/post/{post.id}/change/')
        post.save()
        return True
    except Exception as e:
        return False

def changeTest(post, form, user, tags, correct_ans):
    try:
        profile = Profile.objects.get(user=user)
        post.title = form.cleaned_data['title']
        post.content = form.cleaned_data['content']
        post.is_good_post = False
        post.tags = tags
        post.userJoined = {}
        post.correctAnswers = correct_ans
        if not ((profile.rank == 'A') or (profile.rank == 'T') or (autoPublish(user))):
            post.is_verify = False
            post.is_publish = False
            discord_webhook("Duyệt Bài",
                            f"Link duyệt: {website_URL}/admin/Posts/test/{post.id}/change/ \nLink preview bài viết: {website_URL}/p/kiem_tra/p/{post.test_id}/",
                            "private", f'/admin/Posts/post/{post.id}/change/')
        post.save()
        return True
    except Exception as e:
        print(e)
        return False

def get_correct_answer_from_text(data):
    while (data[0] != '1'):
        data = data[1:]
    arr = data.strip().split('\n')
    char = ['a', 'b', 'c', 'd']
    correct_ans = {}
    cnt = 1
    for i in range(len(arr)):
        arr[i] = arr[i].strip()
        if (len(arr[i]) != 2):
            continue
        if not (arr[i][1].lower() in char):
            print('err char')
            return False
        if (int(arr[i][0]) != cnt):
            print('err num')
            return False

        correct_ans[f"question{arr[i][0]}"] = arr[i][1].lower()
        cnt += 1
    return correct_ans