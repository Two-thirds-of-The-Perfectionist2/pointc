# Generated by Django 4.1.5 on 2023-01-23 11:42

from django.conf import settings
import django.contrib.gis.db.models.fields
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
                ('title', models.CharField(max_length=24)),
                ('address', models.CharField(max_length=32)),
                ('location', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('phone', models.CharField(max_length=24)),
                ('category', models.CharField(choices=[('Еда', 'Food'), ('Товары', 'Merchandise'), ('Другое', 'Other')], max_length=24)),
                ('tag', models.CharField(blank=True, max_length=24)),
                ('body', models.TextField(blank=True)),
                ('cover', models.ImageField(default='default/organization.jpg', upload_to='organizations')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organizations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=24)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True)),
                ('cover', models.ImageField(default='default/product.jpg', upload_to='products')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='main.organization')),
            ],
        ),
    ]
