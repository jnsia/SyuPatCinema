# Generated by Django 4.2.7 on 2023-11-21 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_like_genres'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='like_genres',
        ),
    ]
