from django.core.management.base import BaseCommand
from django.utils.text import slugify
from geography.models import GeographicDivision  # Adjust these imports based on your app name
from unidecode import unidecode  # Import unidecode for slug generation


class Command(BaseCommand):
    help = 'Import South Aegean region and municipalities data'

    def handle(self, *args, **options):
        divisions = [
            {"name": "South Aegean", "slug": "", "parent": None, "level_name": "Region"},
            {"name": "Municipality of Agathonisi", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Amorgos", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Andros", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Astypalaia", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Halki", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Kalymnos", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Karpathos", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Kasos", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Kastellorizo", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Kea", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Kos", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Kythnos", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Leipsoi", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Leros", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Milos", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Mykonos", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Naxos", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Paros", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Patmos", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Rhodes", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Santorini", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Serifos", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Sifnos", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Symi", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Syros", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Tilos", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
            {"name": "Municipality of Tinos", "slug": "", "parent": "south-aegean", "level_name": "Municipality"},
        ]

        # Helper function to generate a unique slug
        def generate_unique_slug(name, parent=None):
            base_slug = slugify(unidecode(name))
            slug = base_slug
            counter = 1
            while GeographicDivision.objects.filter(slug=slug, parent=parent).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            return slug

        # Import divisions
        for item in divisions:
            name = item['name']
            parent_slug = item['parent']
            level_name = item['level_name']

            parent = None
            if parent_slug:
                try:
                    parent = GeographicDivision.objects.get(slug=parent_slug)
                except GeographicDivision.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Parent division with slug "{parent_slug}" does not exist.'))
                    continue

            # Generate a unique slug for the division
            slug = item['slug'] or generate_unique_slug(name, parent)

            # Create or retrieve the division
            division, created = GeographicDivision.objects.get_or_create(
                slug=slug,
                parent=parent,
                defaults={
                    'name': name,
                    'level_name': level_name,
                    'confirmed': True,  # Set other non-translated fields as needed
                }
            )

            # Log success or warning
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created division: {name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Division already exists: {name}'))

        self.stdout.write(self.style.SUCCESS('Completed importing municipalities for South Aegean'))
