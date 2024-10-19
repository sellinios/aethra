from django.core.management.base import BaseCommand
from django.utils.text import slugify
from geography.models import GeographicDivision  # Adjust these imports based on your app name
from unidecode import unidecode  # Import unidecode for slug generation


class Command(BaseCommand):
    help = 'Import Western Macedonia region and municipalities data'

    def handle(self, *args, **options):
        divisions = [
            {"name": "Western Macedonia", "slug": "", "parent": None, "level_name": "Region"},
            {"name": "Municipality of Amyntaio", "slug": "", "parent": "western-macedonia",
             "level_name": "Municipality"},
            {"name": "Municipality of Argos Orestiko", "slug": "", "parent": "western-macedonia",
             "level_name": "Municipality"},
            {"name": "Municipality of Deskati", "slug": "", "parent": "western-macedonia",
             "level_name": "Municipality"},
            {"name": "Municipality of Eordaia", "slug": "", "parent": "western-macedonia",
             "level_name": "Municipality"},
            {"name": "Municipality of Florina", "slug": "", "parent": "western-macedonia",
             "level_name": "Municipality"},
            {"name": "Municipality of Grevena", "slug": "", "parent": "western-macedonia",
             "level_name": "Municipality"},
            {"name": "Municipality of Kozani", "slug": "", "parent": "western-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Nestorio", "slug": "", "parent": "western-macedonia",
             "level_name": "Municipality"},
            {"name": "Municipality of Prespes", "slug": "", "parent": "western-macedonia",
             "level_name": "Municipality"},
            {"name": "Municipality of Servia", "slug": "", "parent": "western-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Velventos", "slug": "", "parent": "western-macedonia",
             "level_name": "Municipality"},
            {"name": "Municipality of Voio", "slug": "", "parent": "western-macedonia", "level_name": "Municipality"},
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


