# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-20 10:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0004_auto_20170517_1535'),
    ]

    operations = [
        migrations.RenameField(
            model_name='h_lifelogs',
            old_name='hf_artile_cate',
            new_name='cate',
        ),
        migrations.RenameField(
            model_name='h_lifelogs',
            old_name='hf_artile_content',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='h_lifelogs',
            old_name='hf_artile_time',
            new_name='time',
        ),
        migrations.RenameField(
            model_name='h_lifelogs',
            old_name='hf_artile_title',
            new_name='title',
        ),
        migrations.AddField(
            model_name='h_lifelogs',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to=b'', verbose_name='\u65e5\u5fd7\u56fe\u7247'),
        ),
        migrations.AlterField(
            model_name='h_frontnotes',
            name='hf_artile_cate',
            field=models.ForeignKey(max_length=20, on_delete=django.db.models.deletion.CASCADE, to='myweb.hf_artile_sort', verbose_name='\u5206\u7c7b'),
        ),
        migrations.AlterField(
            model_name='h_frontnotes',
            name='hf_artile_img',
            field=models.ImageField(blank=True, null=True, upload_to=b'', verbose_name='\u6587\u7ae0\u56fe\u7247'),
        ),
        migrations.AlterField(
            model_name='hf_artile_sort',
            name='hf_sort_describe',
            field=models.TextField(blank=True, null=True, verbose_name='\u5206\u7c7b\u63cf\u8ff0'),
        ),
    ]
