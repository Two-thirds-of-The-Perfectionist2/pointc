# Generated by Django 4.1.5 on 2023-01-16 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_alter_user_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='cover',
            new_name='picture',
        ),
    ]
