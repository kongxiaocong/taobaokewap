# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class lunbotu(models.Model):
    title=models.CharField(max_length=200)
    couponUrl = models.CharField(max_length=200)
    imageUrl = models.CharField(max_length=200)
    def __unicode__(self):
        return self.title

class jdcookie(models.Model):
    title=models.CharField(max_length=200)
    cookies = models.CharField(max_length=2500)
    def __unicode__(self):
        return self.title
