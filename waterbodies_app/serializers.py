from rest_framework import serializers
from .models import WaterBody

class WaterBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterBody
        fields = '__all__'