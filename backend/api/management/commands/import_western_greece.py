from django.core.management.base import BaseCommand
from django.utils.text import slugify
from geography.models import GeographicDivision  # Adjust these imports based on your app name
from unidecode import unidecode  # Import unidecode for slug generation


class Command(BaseCommand):
    help = 'Import Western Greece region and municipalities data'

    def handle(self, *args, **options):
        divisions = [
            {"name": "Western Greece", "slug": "", "parent": None, "level_name": "Region"},
            {"name": "Municipality of Agrinio", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Aigialeia", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Aktio-Vonitsa", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Amfilochia", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Andravida-Kyllini", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Andritsaina-Krestena", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Erymanthos", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Ilida", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Kalavryta", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Missolonghi", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Nafpaktia", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Olympia", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Patras", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Pineios", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Pyrgos", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Thermo", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of West Achaea", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Xiromero", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Zacharo", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
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

        self.stdout.write(self.style.SUCCESS('Completed importing municipalities for Western Greece'))
