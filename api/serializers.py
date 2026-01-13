# api/serializers.py
from rest_framework import serializers
from .models import CVERecord

class CVERecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVERecord
        fields = "__all__"
