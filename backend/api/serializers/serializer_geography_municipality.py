from rest_framework import serializers
from geography.models.model_geographic_division import GeographicDivision, Municipality

class MunicipalitySerializer(serializers.ModelSerializer):
    population = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()

    class Meta:
        model = GeographicDivision  # Still use the parent model
        fields = ['id', 'name', 'population', 'area', 'confirmed', 'level_name', 'parent']  # Adjust fields as necessary

    def get_population(self, obj):
        # Check if the instance is a Municipality and return its population
        if isinstance(obj, Municipality):
            return obj.population
        return None

    def get_area(self, obj):
        # Check if the instance is a Municipality and return its area
        if isinstance(obj, Municipality):
            return obj.area
        return None
