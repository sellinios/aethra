# api/views/view_geography_planet.py

from rest_framework.response import Response
from rest_framework.decorators import api_view
from geography.models.model_geographic_planet import GeographicPlanet
from api.serializers.serializer_geography_planet import SerializerGeographicPlanet
from rest_framework import status

@api_view(['GET'])
def planet_list(request):
    """
    Retrieve a list of all planets.
    """
    planets = GeographicPlanet.objects.all()
    serializer = SerializerGeographicPlanet(planets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def planet_count(request):
    """
    Retrieve the total number of planets.
    """
    count = GeographicPlanet.objects.count()
    return Response({'planet_count': count}, status=status.HTTP_200_OK)
