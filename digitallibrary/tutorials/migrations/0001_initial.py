# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-27 12:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_title', models.CharField(max_length=250)),
                ('book_author', models.CharField(max_length=250)),
                ('pdf_file', models.FileField(upload_to=b'')),
                ('is_favourite', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SoftwareTutorials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=250)),
                ('language_description', models.TextField()),
                ('creator', models.CharField(max_length=250)),
                ('lang_logo', models.FileField(upload_to=b'')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='softwaretutorials',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorials.SoftwareTutorials'),
        ),
    ]
