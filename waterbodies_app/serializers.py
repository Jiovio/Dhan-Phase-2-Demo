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