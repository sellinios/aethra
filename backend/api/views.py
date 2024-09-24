# backend/api/views.py

from rest_framework.response import Response
from rest_framework.decorators import api_view
from geography.models.model_geographic_planet import GeographicPlanet

@api_view(['GET'])
def planet_count(request):
    """
    API to return the number of planets in the database.
    """
    count = GeographicPlanet.objects.count()
    return Response({'planet_count': count})
