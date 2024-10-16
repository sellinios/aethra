from rest_framework import serializers
from geography.models.model_geographic_division import GeographicDivision

class MunicipalitySerializer(serializers.ModelSerializer):
    population = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    level_name = serializers.SerializerMethodField()

    class Meta:
        model = GeographicDivision
        fields = ['id', 'name', 'population', 'area', 'confirmed', 'level_name', 'parent']

    def get_population(self, obj):
        return getattr(obj, 'population', None)

    def get_area(self, obj):
        return getattr(obj, 'area', None)

    def get_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True)

    def get_level_name(self, obj):
        return obj.safe_translation_getter('level_name', any_language=True)
