# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-22 06:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo_item', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TodoList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
            ],
        ),
        migrations.AddField(
            model_name='todoitem',
            name='todo_list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='todo_items', to='todo_item.TodoList'),
        ),
    ]
