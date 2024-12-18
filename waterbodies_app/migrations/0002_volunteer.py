# Generated by Django 4.1.4 on 2024-03-10 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waterbodies_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('volunteering_for', models.CharField(choices=[('cleaning_restoring', 'Cleaning and Restoring'), ('water_monitoring', 'Water Ecosystem Monitoring'), ('tree_planting', 'Tree Planting'), ('others', 'Others')], max_length=50)),
                ('taluk', models.CharField(max_length=100)),
                ('block', models.CharField(max_length=100)),
            ],
        ),
    ]
