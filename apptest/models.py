# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class UserInfo(models.Model):
    username = models.CharField(max_length=32,null=False)
    password = models.CharField(max_length=64,null=False)
