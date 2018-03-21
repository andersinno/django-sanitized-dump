# -*- coding: utf-8 -*-
from django.db import models


class Secret(models.Model):
    name = models.CharField(blank=True, max_length=255, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'testapp'


class Name(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'testapp'
