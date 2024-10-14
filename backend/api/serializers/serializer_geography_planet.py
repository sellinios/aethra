from rest_framework import serializers
from geography.models.model_geographic_planet import GeographicPlanet

class SerializerGeographicPlanet(serializers.ModelSerializer):
    class Meta:
        model = GeographicPlanet
        fields = '__all__'  # Adjust as needed
