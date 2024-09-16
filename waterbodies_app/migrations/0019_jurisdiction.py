# Generated by Django 4.1 on 2024-08-30 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waterbodies_app', '0018_district'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jurisdiction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('createdBy', models.CharField(max_length=100)),
            ],
        ),
    ]
