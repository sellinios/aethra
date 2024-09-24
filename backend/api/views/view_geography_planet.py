from rest_framework.response import Response
from rest_framework.decorators import api_view
from geography.models.model_geographic_planet import GeographicPlanet
from api.serializers.serializer_geography_planet import SerializerGeographicPlanet

@api_view(['GET'])
def planet_list(request):
    planets = GeographicPlanet.objects.all()
    serializer = SerializerGeographicPlanet(planets, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def planet_count(request):
    count = GeographicPlanet.objects.count()
    return Response({'planet_count': count})

@api_view(['GET'])
def health_check(request):
    return Response({'status': 'healthy'})
