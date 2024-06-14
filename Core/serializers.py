from rest_framework import serializers
from .models import Operationitem

class OperationItemSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    activity_supplier = serializers.StringRelatedField()
    day = serializers.StringRelatedField()
    tour = serializers.StringRelatedField()
    transfer = serializers.StringRelatedField()
    vehicle = serializers.StringRelatedField()
    supplier = serializers.StringRelatedField()
    hotel = serializers.StringRelatedField()
    activity = serializers.StringRelatedField()
    driver = serializers.StringRelatedField()
    guide = serializers.StringRelatedField()
    new_museum = serializers.StringRelatedField(many=True)
    class Meta:
        model = Operationitem
        fields = '__all__'
