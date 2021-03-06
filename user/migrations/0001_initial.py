# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-04-16 17:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('username', models.CharField(max_length=11, verbose_name='用户名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=11)),
                ('is_avtive', models.BooleanField(default=False, verbose_name='激活状态')),
            ],
            options={
                'db_table': 'user_user_profile',
            },
        ),
    ]
