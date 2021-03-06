from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    nickname = models.CharField(max_length=50)
    sex = models.CharField(max_length=1)
    birthday = models.DateField()
    last_login = models.DateTimeField(default=timezone.now())
    is_superuser = models.IntegerField(default=0)
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField(default=1)
    is_active = models.IntegerField(default=1)
    date_joined = models.DateTimeField()
    verify_msg = models.CharField(max_length=50)
    update_time = models.DateTimeField()
    country = models.CharField(max_length=45)
    school = models.CharField(max_length=45)

    class Meta:
        db_table = 'user'


class Operating(models.Model):
    operation_cn = models.CharField(max_length=50)
    operation_en = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    parent_id = models.IntegerField()
    is_root = models.CharField(max_length=1)

    class Meta:
        db_table = 'operating'


class Jurisdiction(models.Model):
    user_id = models.IntegerField()
    operating_id = models.IntegerField()

    class Meta:
        db_table = 'jurisdiction'


class News(models.Model):
    user_id = models.IntegerField()
    title = models.CharField(max_length=50)
    keyword = models.CharField(max_length=50)
    article = models.TextField()
    state = models.IntegerField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    push_time = models.DateTimeField()

    class Meta:
        db_table = 'news'


class Relationship(models.Model):
    user_id = models.IntegerField()
    friend_id = models.IntegerField()
    create_time = models.DateTimeField()

    class Meta:
        db_table = 'relationship'


class Message(models.Model):
    from_user_id = models.IntegerField()
    to_user_id = models.IntegerField()
    message = models.CharField(max_length=400)
    state = models.CharField(max_length=1)
    type = models.CharField(max_length=1)
    create_time = models.DateTimeField()
    read_time = models.DateTimeField()

    class Meta:
        db_table = 'message'


class Question(models.Model):
    user_id = models.IntegerField()
    title = models.CharField(max_length=400)
    question = models.CharField(max_length=400)
    state = models.CharField(max_length=1)
    create_time = models.DateTimeField()
    category_id = models.IntegerField()
    answer_num = models.IntegerField()

    class Meta:
        db_table = 'question'


class Answer(models.Model):
    question_id = models.IntegerField()
    user_id = models.IntegerField()
    like_num = models.IntegerField()
    create_time = models.DateTimeField()
    answer = models.CharField(max_length=400)

    class Meta:
        db_table = 'answer'


class LikeAnswer(models.Model):
    user_id = models.IntegerField()
    answer_id = models.IntegerField()

    class Meta:
        db_table = 'like_answer'


class Location(models.Model):
    continent = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    school = models.CharField(max_length=50)
    is_root = models.CharField(max_length=1)
    parent_id = models.IntegerField()
    level = models.CharField(max_length=1)

    class Meta:
        db_table = 'location'


class NewsKeyword(models.Model):
    keyword = models.CharField(max_length=50)
    type = models.CharField(max_length=1)

    class Meta:
        db_table = 'news_keyword'


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    news_id = models.IntegerField()
    user_id = models.IntegerField()
    comment = models.CharField(max_length=200)
    create_time = models.DateTimeField()

    class Meta:
        db_table = 'comment'


class ReplyComment(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    comment_id = models.IntegerField()
    reply = models.CharField(max_length=200)
    create_time = models.DateTimeField()

    class Meta:
        db_table = 'reply_comment'


class QuestionCategory(models.Model):
    category = models.CharField(max_length=45)

    class Meta:
        db_table = 'question_category'