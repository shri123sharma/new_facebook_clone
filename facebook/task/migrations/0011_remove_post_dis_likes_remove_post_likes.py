# Generated by Django 4.1 on 2022-08-25 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0010_post_dis_likes_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='dis_likes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]