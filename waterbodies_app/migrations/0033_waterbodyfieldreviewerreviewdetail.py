# Generated by Django 4.2.16 on 2024-10-22 05:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('waterbodies_app', '0032_tankdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaterBodyFieldReviewerReviewDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('surveyNumber', models.CharField(blank=True, max_length=255)),
                ('waterBodyAvailability', models.BooleanField(default=True)),
                ('waterbodyType', models.CharField(blank=True, max_length=255)),
                ('waterbodyId', models.CharField(blank=True, max_length=255)),
                ('waterbodyName', models.CharField(blank=True, max_length=255)),
                ('district', models.CharField(blank=True, max_length=255)),
                ('taluk', models.CharField(blank=True, max_length=255)),
                ('block', models.CharField(blank=True, max_length=255)),
                ('panchayat', models.CharField(blank=True, max_length=255)),
                ('village', models.CharField(blank=True, max_length=255)),
                ('jurisdiction', models.CharField(blank=True, max_length=255)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('ward', models.CharField(blank=True, max_length=255)),
                ('waterParams', models.JSONField()),
                ('gpsCordinates', models.JSONField()),
                ('draft_status', models.IntegerField()),
                ('verify_status', models.IntegerField()),
                ('createdBy', models.CharField(max_length=255)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('lastModifiedBy', models.CharField(blank=True, max_length=255)),
                ('lastModifiedDate', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]