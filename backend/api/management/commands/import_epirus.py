from django.core.management.base import BaseCommand
from django.utils.text import slugify
from geography.models import GeographicDivision  # Adjust these imports based on your app name
from unidecode import unidecode  # Import unidecode


class Command(BaseCommand):
    help = 'Import Epirus region and municipalities data'

    def handle(self, *args, **options):
        divisions = [
            {"name": "Epirus", "slug": "", "parent": None, "level_name": "Region"},
            {"name": "Municipality of Arta", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Central Tzoumerka", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Dodoni", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Filiates", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Georgios Karaiskakis", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Igoumenitsa", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Ioannina", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Konitsa", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Metsovo", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Nikolaos Skoufas", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of North Tzoumerka", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Parga", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Pogoni", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Preveza", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Souli", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Zagori", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Ziros", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Zitsa", "slug": "", "parent": "epirus", "level_name": "Municipality"},
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
            slug = generate_unique_slug(name, parent)

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

        self.stdout.write(self.style.SUCCESS('Completed importing municipalities for Epirus'))
