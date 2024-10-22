# waterbodies_app/models.py

from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
class Pond(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    district = models.CharField(max_length=100)
    taluk = models.CharField(max_length=100)
    block = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    waterbody_type = models.CharField(max_length=100)
    waterbody_id = models.CharField(max_length=100)
    survey_number = models.CharField(max_length=100)
    ownership = models.CharField(max_length=100)
    availability = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Tank(models.Model):
    tank_name = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    taluk = models.CharField(max_length=100)
    block = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    jurisdiction_name = models.CharField(max_length=100)
    ward = models.CharField(max_length=100)
    waterbody_type = models.CharField(max_length=100)
    waterbody_id = models.CharField(max_length=100)
    survey_number = models.CharField(max_length=100)
    ownership = models.CharField(max_length=100)
    waterbody_availability = models.CharField(max_length=100)

    def __str__(self):
        return self.tank_name
    
class TempleTank(models.Model):
    waterbody_name = models.CharField(max_length=255)
    jurisdiction_name = models.CharField(max_length=255)
    ward = models.CharField(max_length=255)
    waterbody_type = models.CharField(max_length=255)
    waterbody_id = models.CharField(max_length=255, unique=True)
    survey_number = models.CharField(max_length=255)
    ownership = models.CharField(max_length=255)
    waterbody_availability = models.BooleanField()

    def __str__(self):
        return self.waterbody_name
    
class Oorani(models.Model):
    waterbody_name = models.CharField(max_length=255)
    jurisdiction_name = models.CharField(max_length=255)
    ward = models.CharField(max_length=255)
    waterbody_type = models.CharField(max_length=255)
    waterbody_id = models.CharField(max_length=255, unique=True)
    survey_number = models.CharField(max_length=255)
    ownership = models.CharField(max_length=255)
    waterbody_availability = models.BooleanField()

    def __str__(self):
        return self.waterbody_name
    

class KMLFilesz(models.Model):
    name = models.CharField(max_length=255)
    kml_file = models.FileField(upload_to='kml_files/')
    original_kmz_file = models.FileField(upload_to='kmz_files/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class PoOwaterbody(models.Model):
    unique_id = models.CharField(max_length=255) 
    ponds_oo = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    taluk = models.CharField(max_length=255, null=True, blank=True)
    block = models.CharField(max_length=255, null=True, blank=True)
    panchayat = models.CharField(max_length=255, null=True, blank=True)
    village = models.CharField(max_length=255, null=True, blank=True)
    pond_type = models.CharField(max_length=255, null=True, blank=True)
    cap_mcm = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    fpl_m = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    mwl_m = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pbl_m = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sto_dep_m = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    catchment = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    wat_spr_ar = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    bund_len_m = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    dis_cusecs = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)

    def __str__(self):
        return self.unique_id
    
class WaterbodiesTank(models.Model):
    district = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    block = models.CharField(max_length=255, null=True, blank=True)
    panchayat = models.CharField(max_length=255, null=True, blank=True)
    village = models.CharField(max_length=255, null=True, blank=True)
    tank_name = models.CharField(max_length=255, null=True, blank=True)
    tank_type = models.CharField(max_length=255, null=True, blank=True)
    ayacut_ha = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    wat_spr_ar = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cap_mcm = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    no_of_sluices = models.IntegerField(null=True, blank=True)
    sluices_type = models.CharField(max_length=255, null=True, blank=True)
    bund_len_m = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tbl_m = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    mwl_m = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ftl_m = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    unique_id = models.CharField(max_length=255)
    sto_depth_m = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    catchment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    no_of_weirs = models.IntegerField(null=True, blank=True)
    weir_length_m = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    low_sill_m = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    dis_cusecs = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)

    def __str__(self):
        return self.unique_id
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class District(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Jurisdiction(models.Model):
    code = models.CharField(max_length=50, unique=True)
    createdBy = models.CharField(max_length=100)

    def __str__(self):
        return self.code
    
class Taluk(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    district_id = models.CharField(max_length=10)  # Keeping district_id as a CharField or IntegerField

    def __str__(self):
        return self.name
    
class FenceType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Availability(models.Model):
    name= models.CharField(max_length=100)
    
    def __str__(self):
        return self.name    
class Habitation(models.Model):
    district_code = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
    block_code = models.CharField(max_length=10)
    block = models.CharField(max_length=100)
    village_code = models.CharField(max_length=10)
    village = models.CharField(max_length=100)
    habitation_code = models.CharField(max_length=10)
    habitation = models.CharField(max_length=100)

    def __str__(self):
        return self.habitation
class UrbanLocalBodies(models.Model):
    type_code = models.CharField(max_length=50)  # TypeCode
    type = models.CharField(max_length=100)  # Type
    name = models.CharField(max_length=100)  # Name
    ward_code = models.CharField(max_length=50)  # WardCode
    ward = models.CharField(max_length=100)  # Ward

    def __str__(self):
        return self.type_code
class AyacutNonCultivation(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class BoundaryDropPoints(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class BundIssues(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class BarrelType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
 
class BundFunctionalities(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Conditions(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    


class CatchmentType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class TankData(models.Model):
    tank_num = models.CharField(max_length=100)  # TANK_NUM
    unique_id = models.CharField(max_length=100)  # Unique_id
    tank_name = models.CharField(max_length=200)  # Tank_Name
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # Latitude
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # Longitude
    village = models.CharField(max_length=200)  # Village
    block = models.CharField(max_length=200)  # Block
    taluk = models.CharField(max_length=200)  # Taluk
    district = models.CharField(max_length=200)  # District
    subbasin = models.CharField(max_length=200)  # Subbasin
    basin = models.CharField(max_length=200)  # Basin
    section = models.CharField(max_length=200)  # Section
    sub_dn = models.CharField(max_length=200)  # Sub_Dn
    division = models.CharField(max_length=200)  # Division
    circle = models.CharField(max_length=200)  # Circle
    region = models.CharField(max_length=200)  # Region
    tank_type = models.CharField(max_length=100)  # Tank_Type
    cap_mcm = models.DecimalField(max_digits=10, decimal_places=3)  # Cap_MCM
    ftl_m = models.DecimalField(max_digits=6, decimal_places=3)  # FTL_m
    mwl_m = models.DecimalField(max_digits=6, decimal_places=3)  # MWL_m
    tbl_m = models.DecimalField(max_digits=6, decimal_places=3)  # TBL_m
    sto_dep_m = models.DecimalField(max_digits=6, decimal_places=3)  # Sto_Dep_m
    ayacut_ha = models.DecimalField(max_digits=10, decimal_places=3)  # Ayacut_ha
    catch_sqkm = models.DecimalField(max_digits=10, decimal_places=3)  # Catch_sqkm
    wat_spr_ha = models.DecimalField(max_digits=10, decimal_places=3)  # Wat_Spr_ha
    no_of_weir = models.IntegerField()  # No_of_Weir
    weir_len_m = models.DecimalField(max_digits=10, decimal_places=3)  # Weir_Len_m
    no_sluice = models.IntegerField()  # No_Sluice
    low_sil_m = models.DecimalField(max_digits=10, decimal_places=3)  # Low_Sil_m
    bund_len_m = models.DecimalField(max_digits=10, decimal_places=3)  # Bund_Len_m
    dis_cusec = models.DecimalField(max_digits=10, decimal_places=3)  # Dis_cusec

    def __str__(self):
        return self.tank_name
    
class WaterBodyFieldReviewerReviewDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)  # Use uuid4 to generate unique IDs
    surveyNumber = models.CharField(max_length=255, blank=True)
    waterBodyAvailability = models.BooleanField(default=True)
    waterbodyType = models.CharField(max_length=255, blank=True)
    waterbodyId = models.CharField(max_length=255, blank=True)
    waterbodyName = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=255, blank=True)
    taluk = models.CharField(max_length=255, blank=True)
    block = models.CharField(max_length=255, blank=True)
    panchayat = models.CharField(max_length=255, blank=True)
    village = models.CharField(max_length=255, blank=True)
    jurisdiction = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    ward = models.CharField(max_length=255, blank=True)
    waterParams = models.JSONField()
    gpsCordinates = models.JSONField()
    draft_status = models.IntegerField()
    verify_status = models.IntegerField()
    createdBy = models.CharField(max_length=255)
    createdDate = models.DateTimeField(auto_now_add=True)
    lastModifiedBy = models.CharField(max_length=255, blank=True)
    lastModifiedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.waterbodyName