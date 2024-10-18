# api/views/view_geography_municipalities.py

from django.utils.translation import get_language
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from geography.models import GeographicDivision
from api.serializers import MunicipalitySerializer

class MunicipalityList(APIView):
    """
    Retrieve a list of all municipalities.
    """
    def get(self, request):
        language = get_language()
        normalized_language = language.split('-')[0]

        # Query municipalities using Parler's translated method
        municipalities = GeographicDivision.objects.translated(normalized_language).filter(
            translations__level_name="Municipality"
        )

        if not municipalities.exists():
            return Response(
                {"detail": f"No municipalities found for the current language ({normalized_language})."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize the results
        serializer = MunicipalitySerializer(
            municipalities,
            many=True,
            context={'language': normalized_language}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
