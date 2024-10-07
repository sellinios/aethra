from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from geography.models.model_geographic_division import GeographicDivision
from ..serializers.serializer_geography_municipality import MunicipalitySerializer

class MunicipalityList(APIView):
    def get(self, request):
        # Fetch only GeographicDivision objects with level_name='Municipality'
        municipalities = GeographicDivision.objects.filter(level_name="Municipality")
        serializer = MunicipalitySerializer(municipalities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
