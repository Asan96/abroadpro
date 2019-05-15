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

    class Meta:
        db_table = 'user'


class Operating(models.Model):
    operation_cn = models.CharField(max_length=50)
    operation_en = models.CharField(max_length=50)
    url = models.CharField(max_length=50)

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

    class Meta:
        db_table = 'news'