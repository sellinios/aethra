import time
import requests
import logging
import logging.config
import os
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
from geography.models import GeographicPlace

# Configuration Constants
ELEVATION_API_URL = "https://api.open-elevation.com/api/v1/lookup"
ELEVATION_BATCH_SIZE = 1000  # Number of locations per API request
RETRY_LIMIT = 3  # Number of retries for failed API requests
TIMEOUT = 30  # Timeout for API requests in seconds
BULK_UPDATE_BATCH_SIZE = 10000  # Adjusted for better performance

# Configure Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # Preserve existing loggers
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} [{name}:{lineno}] {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(settings.BASE_DIR, 'elevation_update.log'),
            'formatter': 'verbose',
            'mode': 'a',  # Append mode
        },
    },
    'loggers': {
        'elevation_update': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',  # Set to DEBUG for detailed logs
            'propagate': False,
        },
    },
}

# Apply Logging Configuration
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('elevation_update')


def fetch_and_update_elevations(batch):
    """
    Fetch elevations for a batch of places and update the database.
    """
    from geography.models import GeographicPlace  # Import inside function for multiprocessing
    from django.db import transaction

    # Initialize logging for the worker process
    logger = logging.getLogger('elevation_update')

    # Prepare the payload for the API
    locations = [{"latitude": lat, "longitude": lng} for _, lat, lng in batch]
    payload = {"locations": locations}

    retries = 0
    elevations = None

    while retries < RETRY_LIMIT:
        try:
            logger.debug(f'Attempt {retries + 1}: Sending request to Open-Elevation API for batch size {len(batch)}.')
            response = requests.post(ELEVATION_API_URL, json=payload, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            elevations = [result.get('elevation') for result in data.get('results', [])]
            logger.debug(f'Received response from Open-Elevation API: {data}')
            break  # Exit loop if successful
        except Exception as e:
            retries += 1
            logger.error(f'Error fetching elevations (Attempt {retries}/{RETRY_LIMIT}): {e}')
            time.sleep(2 ** retries)  # Exponential backoff

    if elevations is None:
        # All retries failed
        failed_count = len(batch)
        logger.warning(f'All retries failed for batch of size {failed_count}.')
        return {'success': 0, 'failed': failed_count}

    # Prepare updates
    updates = []
    for (place_id, _, _), elevation in zip(batch, elevations):
        if elevation is not None:
            updates.append({'id': place_id, 'elevation': elevation})
        else:
            # If elevation is None, set a default value
            updates.append({'id': place_id, 'elevation': 0})
            logger.debug(f'Elevation is None for place ID {place_id}. Setting elevation to 0.')

    # Bulk update the database
    try:
        with transaction.atomic():
            GeographicPlace.objects.bulk_update(
                [GeographicPlace(id=update['id'], elevation=update['elevation']) for update in updates],
                ['elevation'],
                batch_size=BULK_UPDATE_BATCH_SIZE
            )
        logger.debug(f'Successfully updated {len(updates)} GeographicPlace entries.')
        return {'success': len(updates), 'failed': 0}
    except Exception as e:
        logger.error(f'Error updating elevations in the database: {e}')
        return {'success': 0, 'failed': len(updates)}


class Command(BaseCommand):
    help = 'Fetch elevation data from Open-Elevation API and update GeographicPlace entries.'

    def handle(self, *args, **options):
        start_time = time.time()
        logger.info('Starting elevation update process...')

        # Query all GeographicPlace instances that need elevation updates
        places = GeographicPlace.objects.filter(elevation__isnull=True).only('id', 'latitude', 'longitude')

        total_places = places.count()
        if total_places == 0:
            logger.warning('No GeographicPlace entries require elevation updates.')
            self.stdout.write(self.style.WARNING('No GeographicPlace entries require elevation updates.'))
            return

        logger.info(f'Found {total_places} places to update.')
        self.stdout.write(self.style.SUCCESS(f'Found {total_places} places to update.'))

        # Prepare data for processing: generator of (id, latitude, longitude) tuples
        places_iterator = places.iterator(chunk_size=10000)  # Adjust chunk_size based on memory

        # Process in batches
        batch_size = ELEVATION_BATCH_SIZE
        batches = self.get_batches(places_iterator, batch_size)

        # Initialize counters
        successful_updates = 0
        failed_updates = 0

        # Initialize multiprocessing Pool
        with Pool(processes=cpu_count()) as pool:
            # Initialize tqdm for progress visualization
            with tqdm(total=total_places, desc="Processing Places", unit="places") as pbar:
                # Iterate through batches and process
                for result in pool.imap_unordered(fetch_and_update_elevations, batches):
                    successful_updates += result.get('success', 0)
                    failed_updates += result.get('failed', 0)
                    pbar.update(result.get('success', 0) + result.get('failed', 0))

        end_time = time.time()
        logger.info(f'Elevation update completed. Successfully updated {successful_updates} places.')
        self.stdout.write(
            self.style.SUCCESS(
                f'Elevation update completed. Successfully updated {successful_updates} places.'
            )
        )
        if failed_updates > 0:
            logger.warning(f'Failed to update {failed_updates} places. Check logs for details.')
            self.stdout.write(
                self.style.WARNING(f'Failed to update {failed_updates} places. Check logs for details.')
            )
        logger.info(f'Total time taken: {end_time - start_time:.2f} seconds.')
        self.stdout.write(
            self.style.SUCCESS(f'Total time taken: {end_time - start_time:.2f} seconds.')
        )

    def get_batches(self, iterator, batch_size):
        """
        Generator that yields batches of (id, latitude, longitude) tuples.
        """
        batch = []
        for place in iterator:
            batch.append((place.id, place.latitude, place.longitude))
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch
