# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-24 11:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0008_auto_20170522_2039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='h_smallnotes',
            name='hsn_cate',
        ),
    ]
