# Generated by Django 4.1.4 on 2024-06-05 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waterbodies_app', '0012_templetank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Oorani',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waterbody_name', models.CharField(max_length=255)),
                ('jurisdiction_name', models.CharField(max_length=255)),
                ('ward', models.CharField(max_length=255)),
                ('waterbody_type', models.CharField(max_length=255)),
                ('waterbody_id', models.CharField(max_length=255, unique=True)),
                ('survey_number', models.CharField(max_length=255)),
                ('ownership', models.CharField(max_length=255)),
                ('waterbody_availability', models.BooleanField()),
            ],
        ),
    ]