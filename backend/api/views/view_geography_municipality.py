from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from geography.models.model_geographic_division import Municipality
from ..serializers.serializer_geography_municipality import MunicipalitySerializer

class MunicipalityList(APIView):
    def get(self, request):
        municipalities = Municipality.objects.all()
        serializer = MunicipalitySerializer(municipalities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
