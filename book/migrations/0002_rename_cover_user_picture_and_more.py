# Generated by Django 4.1.5 on 2023-01-17 05:48

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='cover',
            new_name='picture',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_organization',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_worker',
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]
