# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-16 06:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apptest', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='test',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='user_group',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='user_type_id',
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='password',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='username',
            field=models.CharField(max_length=32),
        ),
        migrations.DeleteModel(
            name='UserGroup',
        ),
    ]
