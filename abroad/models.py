from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    sex = models.CharField(max_length=1)
    birthday = models.DateField()
    email = models.CharField(max_length=50)
    verify_msg = models.CharField(max_length=50)
    create_time = models.DateField()
    update_time = models.DateField()

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