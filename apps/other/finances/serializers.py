from rest_framework import serializers
from .models import FinanceSetting, FinanceRecord

class FinanceSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceSetting
        fields = ['id', 'key', 'value', 'updated_at']

class FinanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceRecord
        fields = ['id', 'month', 'year', 'value', 'created_at']
