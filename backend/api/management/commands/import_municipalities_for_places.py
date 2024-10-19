import time
from multiprocessing import Pool, cpu_count
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.db import transaction
from geography.models import GeographicPlace, GeographicDivision

class Command(BaseCommand):
    help = 'Associate GeographicPlace instances with their respective municipalities based on location.'

    def handle(self, *args, **kwargs):
        start_time = time.time()
        self.stdout.write(self.style.NOTICE('Starting association of places with municipalities...'))

        # Fetch all municipalities with boundaries
        self.stdout.write('Fetching all municipalities...')
        municipalities = GeographicDivision.objects.filter(
            translations__level_name='Municipality',
            boundary__isnull=False
        ).only('id', 'boundary')

        if not municipalities.exists():
            self.stdout.write(self.style.ERROR('No municipalities with boundaries found in GeographicDivision.'))
            return

        self.stdout.write(f"Found {municipalities.count()} municipalities.")

        # Fetch all GeographicPlace instances that need association
        places = GeographicPlace.objects.filter(admin_division__isnull=True, location__isnull=False)
        total_places = places.count()

        if total_places == 0:
            self.stdout.write(self.style.WARNING('No GeographicPlace entries require association.'))
            return

        self.stdout.write(self.style.SUCCESS(f'Found {total_places} places to associate.'))

        # Convert municipalities to a list for in-memory access (optional, depending on size)
        municipalities_list = list(municipalities)

        # Define chunk size for batch processing
        chunk_size = 1000
        queryset = places.order_by('id')

        # Process in chunks
        for start in range(0, total_places, chunk_size):
            end = start + chunk_size
            places_chunk = queryset[start:end]
            places_data = list(places_chunk.values('id', 'latitude', 'longitude'))

            # Prepare arguments for multiprocessing
            pool_args = [
                {
                    'id': place['id'],
                    'point': Point(place['longitude'], place['latitude'], srid=4326)
                }
                for place in places_data
            ]

            # Use multiprocessing to handle associations in parallel
            with Pool(processes=cpu_count()) as pool:
                results = pool.map(associate_place, pool_args)

            # Prepare updates
            updates = []
            for result in results:
                if result['municipality_id'] is not None:
                    updates.append(
                        GeographicPlace(id=result['id'], admin_division_id=result['municipality_id'])
                    )

            # Bulk update the database
            if updates:
                with transaction.atomic():
                    GeographicPlace.objects.bulk_update(updates, ['admin_division'])

            # Log progress
            self.stdout.write(self.style.SUCCESS(f'Associated {len(updates)} places in chunk {start} - {end}'))

        end_time = time.time()
        self.stdout.write(
            self.style.SUCCESS(
                f'Completed association in {end_time - start_time:.2f} seconds.'
            )
        )

def associate_place(place):
    """
    Determines the municipality containing the given point.
    """
    place_id = place['id']
    point = place['point']

    try:
        municipality = GeographicDivision.objects.get(
            translations__level_name='Municipality',
            boundary__contains=point
        )
        return {'id': place_id, 'municipality_id': municipality.id}
    except GeographicDivision.DoesNotExist:
        return {'id': place_id, 'municipality_id': None}
    except GeographicDivision.MultipleObjectsReturned:
        # If multiple municipalities contain the point, select the first one
        municipality = GeographicDivision.objects.filter(
            translations__level_name='Municipality',
            boundary__contains=point
        ).first()
        if municipality:
            return {'id': place_id, 'municipality_id': municipality.id}
        else:
            return {'id': place_id, 'municipality_id': None}
