from django.core.management.base import BaseCommand
from django.utils.text import slugify
from geography.models import GeographicDivision  # Adjust these imports based on your app name
from unidecode import unidecode  # Import unidecode for slug generation


class Command(BaseCommand):
    help = 'Import Thessaly region and municipalities data'

    def handle(self, *args, **options):
        divisions = [
            {"name": "Thessaly", "slug": "", "parent": None, "level_name": "Region"},
            {"name": "Municipality of Agia", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Almyros", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Alonnisos", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Argithea", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Elassona", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Farkadona", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Farsala", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Karditsa", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Kileler", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Lake Plastiras", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Larissa", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Meteora", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Mouzaki", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Palamas", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Pyli", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Rigas Feraios", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Skiathos", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Sofades", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of South Pelion", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Tempi", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Trikala", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Tyrnavos", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Volos", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Zagora-Mouresi", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
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

        self.stdout.write(self.style.SUCCESS('Completed importing municipalities for Thessaly'))
