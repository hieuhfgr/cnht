# Generated by Django 4.0.6 on 2023-05-30 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupTag',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_id', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('NumberOfQuestions', models.PositiveIntegerField()),
                ('NumberOfSeen', models.PositiveIntegerField(default=0)),
                ('correctAnswers', models.JSONField(default=dict)),
                ('reportedCount', models.PositiveIntegerField(default=0)),
                ('userJoined', models.JSONField(blank=True, default=dict)),
                ('tags', models.JSONField(blank=True, default=dict)),
                ('is_verify', models.BooleanField(default=False)),
                ('is_publish', models.BooleanField(default=False)),
                ('is_good_test', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Posts.grouptag')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('NumberOfLike', models.PositiveIntegerField(default=0)),
                ('NumberOfDislike', models.PositiveIntegerField(default=0)),
                ('NumberOfSeen', models.PositiveIntegerField(default=0)),
                ('reportedCount', models.PositiveIntegerField(default=0)),
                ('interactiveUsers', models.JSONField(blank=True, default=dict)),
                ('tags', models.JSONField(blank=True, default=dict)),
                ('is_verify', models.BooleanField(default=False)),
                ('is_publish', models.BooleanField(default=False)),
                ('is_good_post', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]