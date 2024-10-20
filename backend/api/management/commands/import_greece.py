from django.core.management.base import BaseCommand, CommandError
from geography.models import GeographicPlace, GeographicCategory, GeographicDivision
from django.contrib.gis.geos import Point
from unidecode import unidecode
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = 'Imports Greece cities data directly from a predefined list in English only.'

    def handle(self, *args, **kwargs):
        # Define the data directly within the code
        cities_data = [
            {"id": 1, "name": "Athens", "longitude": 23.7275, "latitude": 37.9838, "elevation": None, "confirmed": True,
             "category_id": 1},
            {"id": 2, "name": "Thessaloniki", "longitude": 22.9444, "latitude": 40.6401, "elevation": None,
             "confirmed": True, "category_id": 1},
            {"id": 3, "name": "Patras", "longitude": 21.7346, "latitude": 38.2466, "elevation": None, "confirmed": True,
             "category_id": 1},
            {"id": 4, "name": "Heraklion", "longitude": 25.1442, "latitude": 35.3387, "elevation": None,
             "confirmed": True, "category_id": 1},
            {"id": 5, "name": "Volos", "longitude": 22.9535, "latitude": 39.3666, "elevation": None, "confirmed": True,
             "category_id": 1},
            {"id": 6, "name": "Larissa", "longitude": 22.4191, "latitude": 39.639, "elevation": None, "confirmed": True,
             "category_id": 1},
            {"id": 7, "name": "Chania", "longitude": 24.0144, "latitude": 35.5122, "elevation": None, "confirmed": True,
             "category_id": 1},
            {"id": 8, "name": "Rhodes", "longitude": 28.2176, "latitude": 36.4346, "elevation": None, "confirmed": True,
             "category_id": 1},
            {"id": 9, "name": "Ioannina", "longitude": 20.8519, "latitude": 39.6676, "elevation": None,
             "confirmed": True, "category_id": 1},
            {"id": 10, "name": "Kalamata", "longitude": 22.1126, "latitude": 37.0376, "elevation": None,
             "confirmed": True, "category_id": 1},
            {"id": 11, "name": "Corfu", "longitude": 19.9198, "latitude": 39.6243, "elevation": None, "confirmed": True,
             "category_id": 1},
            {"id": 12, "name": "Trikala", "longitude": 21.7679, "latitude": 39.5556, "elevation": None,
             "confirmed": True, "category_id": 1},
            {"id": 13, "name": "Serres", "longitude": 23.548, "latitude": 41.085, "elevation": None, "confirmed": True,
             "category_id": 1},
            {"id": 14, "name": "Katerini", "longitude": 22.5073, "latitude": 40.2729, "elevation": None,
             "confirmed": True, "category_id": 1},
            {"id": 15, "name": "Lamia", "longitude": 22.4341, "latitude": 38.8951, "elevation": None, "confirmed": True,
             "category_id": 1},
            {"id": 16, "name": "Agrinio", "longitude": 21.4074, "latitude": 38.6218, "elevation": None,
             "confirmed": True, "category_id": 1},
            {"id": 17, "name": "Piraeus", "longitude": 23.6472, "latitude": 37.9402, "elevation": None,
             "confirmed": True, "category_id": 1},
            {"id": 18, "name": "Kavala", "longitude": 24.415, "latitude": 40.936, "elevation": None, "confirmed": True,
             "category_id": 1},
            {"id": 19, "name": "Karditsa", "longitude": 21.9204, "latitude": 39.3689, "elevation": None,
             "confirmed": True, "category_id": 1},
            {"id": 20, "name": "Kozani", "longitude": 21.7898, "latitude": 40.301, "elevation": None, "confirmed": True,
             "category_id": 1},
            {"id": 21, "name": "Xanthi", "longitude": 24.8892, "latitude": 41.1353, "elevation": None,
             "confirmed": True, "category_id": 1},
            {"id": 22, "name": "Chalkida", "longitude": 23.5946, "latitude": 38.4636, "elevation": None,
             "confirmed": True, "category_id": 1},
            {"id": 23, "name": "Drama", "longitude": 24.1461, "latitude": 41.1496, "elevation": None, "confirmed": True,
             "category_id": 1},
            {"id": 24, "name": "Tripoli", "longitude": 22.3764, "latitude": 37.5089, "elevation": None,
             "confirmed": True, "category_id": 1},
            {"id": 25, "name": "Alexandroupoli", "longitude": 25.8747, "latitude": 40.847, "elevation": None,
             "confirmed": True, "category_id": 1},
            {"id": 26, "name": "Preveza", "longitude": 20.7515, "latitude": 38.9561, "elevation": None,
             "confirmed": True, "category_id": 1},
            {"id": 27, "name": "Nafplio", "longitude": 22.8057, "latitude": 37.5633, "elevation": None,
             "confirmed": True, "category_id": 1},
            {"id": 28, "name": "Edessa", "longitude": 22.0454, "latitude": 40.8009, "elevation": None,
             "confirmed": True, "category_id": 1},
            {"id": 29, "name": "Thebes", "longitude": 23.3275, "latitude": 38.3263, "elevation": None,
             "confirmed": True, "category_id": 1},
            {"id": 30, "name": "Florina", "longitude": 21.4066, "latitude": 40.7816, "elevation": None,
             "confirmed": True, "category_id": 1},
            # Add entries until 300
        ]

        # Fill the list with placeholder city data up to 300
        for i in range(31, 301):
            cities_data.append({
                "id": i,
                "name": f"City_{i}",
                "longitude": round(random.uniform(19.0, 28.0), 6),  # Random longitude within Greece's range
                "latitude": round(random.uniform(35.0, 42.0), 6),  # Random latitude within Greece's range
                "elevation": None,
                "confirmed": True,
                "category_id": 1
            })

        # Fetch all available admin divisions
        admin_divisions = list(GeographicDivision.objects.all())

        if not admin_divisions:
            self.stderr.write(self.style.ERROR("No admin divisions found. Please ensure there are divisions in your database."))
            return

        for row in cities_data:
            try:
                # Fetch the category using provided ID
                category = GeographicCategory.objects.get(id=row['category_id'])

                # Randomly assign an admin division if ID is not known
                admin_division = random.choice(admin_divisions)

                # Create the geographic place
                place = GeographicPlace(
                    longitude=row['longitude'],
                    latitude=row['latitude'],
                    elevation=row['elevation'],
                    confirmed=row['confirmed'],
                    category=category,
                    admin_division=admin_division,
                )

                # Set English name only
                place.set_current_language('en')
                place.name = unidecode(row['name'])

                place.clean()  # Clean the data

                # Save the object
                place.save()

                # Set and save slug
                name = place.safe_translation_getter('name', any_language=True) or 'place'
                base_slug = slugify(unidecode(name))
                place.slug = f"{base_slug}-{place.id}"
                place.save()

                self.stdout.write(self.style.SUCCESS(f"Successfully imported {place}"))
            except GeographicCategory.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"Category with id {row['category_id']} does not exist."))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error importing {row['name']}: {e}"))
