from rest_framework import serializers
from .models import WaterBody

class WaterBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterBody
        fields = '__all__'
        
from .models import WaterBodyFieldReviewerReviewDetail

class WaterBodyFieldReviewerReviewDetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterBodyFieldReviewerReviewDetail
        fields = '__all__'
        

class WaterBodyFieldReviewerReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterBodyFieldReviewerReviewDetail
        fields = '__all__'
        
from .models import TankData

class TankDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TankData
        fields = '__all__'  # Include all fields or specify only those you need
        
from .models import WaterbodiesTank

class WaterbodiesTankSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterbodiesTank
        fields = '__all__'  # Include all fields in the API response
        
from .models import PoOwaterbody

class PoOwaterbodySerializer(serializers.ModelSerializer):
    class Meta:
        model = PoOwaterbody
        fields = '__all__'  # Include all fields in the API response
        
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'first_name', 'last_name', 'email', 'mobile_number', 'address', 'role', 'pincode']
