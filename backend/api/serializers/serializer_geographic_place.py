# api/serializers/serializer_geography_place.py

from rest_framework import serializers
from geography.models.model_geographic_place import GeographicPlace

class GeographicPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeographicPlace
        fields = '__all__'  # Adjust fields as necessary
