from django.core.management.base import BaseCommand
from django.utils.text import slugify
from geography.models import GeographicDivision  # Adjust these imports based on your app name
from unidecode import unidecode  # Import unidecode for slug generation


class Command(BaseCommand):
    help = 'Import Peloponnese region and municipalities data'

    def handle(self, *args, **options):
        divisions = [
            {"name": "Peloponnese", "slug": "", "parent": None, "level_name": "Region"},
            {"name": "Municipality of Argos-Mykines", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Argos", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Corinth", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of East Mani", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Epidaurus", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Ermionida", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Evrotas", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Gortynia", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Kalamata", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Megalopolis", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Messini", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Monemvasia", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Nafplion", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Nemea", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of North Kynouria", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Oichalia", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Pylos-Nestor", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Sikyona", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of South Kynouria", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Sparta", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Trifylia", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Tripoli", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Velo-Vocha", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of West Mani", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Xylokastro-Evrostina", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
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

        self.stdout.write(self.style.SUCCESS('Completed importing municipalities for Peloponnese'))
