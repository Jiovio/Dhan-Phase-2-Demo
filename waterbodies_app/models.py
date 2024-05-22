# waterbodies_app/models.py

from django.db import models

class WaterBody(models.Model):
    Tank_Name = models.CharField(max_length=255)
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    Cap_MCM = models.FloatField()
    Block = models.CharField(max_length=255)
    Taluk = models.CharField(max_length=255)
    District = models.CharField(max_length=255)
    
class Volunteer(models.Model):
    VOLUNTEERING_CHOICES = [
        ('cleaning_restoring', 'Cleaning and Restoring'),
        ('water_monitoring', 'Water Ecosystem Monitoring'),
        ('tree_planting', 'Tree Planting'),
        ('others', 'Others'),
    ]

    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    volunteering_for = models.CharField(max_length=50, choices=VOLUNTEERING_CHOICES)
    taluk = models.CharField(max_length=100)
    block = models.CharField(max_length=100)

    def __str__(self):
        return self.Tank_Name

class Worker(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
class FieldWorker(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    REQUIRED_FIELDS = ['email', 'mobile']
    USERNAME_FIELD = 'username'  
    def __str__(self):
        return self.username