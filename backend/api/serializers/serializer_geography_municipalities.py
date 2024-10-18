# api/serializers.py

from rest_framework import serializers
from geography.models import GeographicDivision

class MunicipalitySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = GeographicDivision
        fields = ['name', 'slug']

    def get_name(self, obj):
        language = self.context.get('language', 'en')
        return obj.safe_translation_getter('name', language_code=language, any_language=True)
