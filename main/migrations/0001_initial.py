# Generated by Django 4.1.5 on 2023-01-17 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=14)),
                ('category', models.CharField(choices=[('Еда', 'Food'), ('Товары', 'Merchandise'), ('Другое', 'Other')], max_length=20)),
                ('tag', models.CharField(max_length=30)),
                ('body', models.TextField()),
                ('cover', models.ImageField(upload_to='organizations')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('cover', models.ImageField(upload_to='products')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organizations', to='main.organization')),
            ],
        ),
    ]
