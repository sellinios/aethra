from rest_framework import serializers
from geography.models.model_geographic_division import Municipality

class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = '__all__'  # Adjust fields as necessary
