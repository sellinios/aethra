from django.core.management.base import BaseCommand
from django.utils.text import slugify
from geography.models import GeographicDivision  # Adjust these imports based on your app name
from unidecode import unidecode  # Import unidecode for slug generation


class Command(BaseCommand):
    help = 'Import Eastern Macedonia and Thrace region and municipalities data'

    def handle(self, *args, **options):
        divisions = [
            {"name": "Eastern Macedonia and Thrace", "slug": "eastern-macedonia-and-thrace", "parent": None, "level_name": "Region"},
            {"name": "Municipality of Abdera", "slug": "abdera", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Alexandroupolis", "slug": "alexandroupolis", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Arriana", "slug": "arriana", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Didymoteicho", "slug": "didymoteicho", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Doxato", "slug": "doxato", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Drama", "slug": "drama", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Iasmos", "slug": "iasmos", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Kato Nevrokopi", "slug": "kato-nevrokopi", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Kavala", "slug": "kavala", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Komotini", "slug": "komotini", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Maroneia-Sapes", "slug": "maroneia-sapes", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Myki", "slug": "myki", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Nestos", "slug": "nestos", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Pangaio", "slug": "pangaio", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Paranesti", "slug": "paranesti", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Prosotsani", "slug": "prosotsani", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Samothrace", "slug": "samothrace", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Soufli", "slug": "soufli", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Thasos", "slug": "thasos", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Topeiros", "slug": "topeiros", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Xanthi", "slug": "xanthi", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
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

        self.stdout.write(self.style.SUCCESS('Completed importing municipalities for Eastern Macedonia and Thrace'))
