# Generated by Django 4.1.5 on 2023-01-16 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cover',
            field=models.ImageField(upload_to='profile_picture'),
        ),
    ]
