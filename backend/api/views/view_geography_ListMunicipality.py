# api/views/view_geography_municipality.py

from django.utils.translation import get_language
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from geography.models.model_geographic_division import GeographicDivision
from ..serializers.serializer_geography_ListMunicipality import MunicipalitySerializer

class MunicipalityList(APIView):
    """
    Retrieve a list of all municipalities.
    """
    def get(self, request):
        # Get the current language (this will query the translations table)
        language = get_language()
        print(f"Current language: {language}")  # Log the language being used

        # Normalize language to handle language codes like 'en-us' or 'en-GB'
        normalized_language = language.split('-')[0]  # Extract 'en' from 'en-us'
        print(f"Normalized language: {normalized_language}")

        # Query using Parler's translated method
        municipalities = GeographicDivision.objects.translated(normalized_language).filter(
            translations__level_name="Municipality"
        )

        # Check if municipalities were found
        if not municipalities.exists():
            return Response(
                {"detail": f"No municipalities found for the current language ({normalized_language})."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize the results
        serializer = MunicipalitySerializer(municipalities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)