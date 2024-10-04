# Generated by Django 4.1 on 2024-08-31 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waterbodies_app', '0019_jurisdiction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Taluk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('district_id', models.CharField(max_length=10)),
            ],
        ),
    ]