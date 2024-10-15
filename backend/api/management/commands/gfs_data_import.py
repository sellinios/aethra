import os
import logging
import pygrib
import numpy as np
from datetime import datetime, timezone, timedelta
from django.contrib.gis.geos import Point as GEOSPoint
from django.core.management.base import BaseCommand
from weather.models.model_gfs_forecast import GFSForecast
from geography.models.model_geographic_place import GeographicPlace
from scipy.spatial import cKDTree
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_forecast_details_from_filename(filename):
    try:
        base_name = os.path.basename(filename)
        parts = base_name.split('_')

        if parts[0] == 'filtered':
            date_str = parts[1]  # e.g., '20241014'
            time_str = parts[2]  # e.g., '1100' or '110000'
            forecast_hour_str = parts[3].split('.')[0]  # e.g., 'f005'

            # Clean time_str to remove any non-digit characters
            time_str_cleaned = re.sub(r'\D', '', time_str)
            time_str_length = len(time_str_cleaned)

            datetime_str = f"{date_str}{time_str_cleaned}"

            # Decide format string based on length of time_str
            if time_str_length == 4:
                format_str = '%Y%m%d%H%M'
            elif time_str_length == 6:
                format_str = '%Y%m%d%H%M%S'
            else:
                logger.error(f"Unexpected time format in filename {filename}: {time_str}")
                return None, None

            # Parse valid datetime
            valid_datetime = datetime.strptime(datetime_str, format_str).replace(tzinfo=timezone.utc)

            # Extract forecast hour (remove 'f' and convert to integer)
            forecast_hour = int(forecast_hour_str.lstrip('f'))

            # Calculate cycle datetime by subtracting forecast hour
            cycle_datetime = valid_datetime - timedelta(hours=forecast_hour)

            # Extract UTC cycle time as a string (e.g., '00', '06', '12', '18')
            utc_cycle_time = cycle_datetime.strftime('%H')

            return valid_datetime, utc_cycle_time
        else:
            logger.error(f"Unexpected filename format: {filename}")
            return None, None
    except Exception as e:
        logger.error(f"Error extracting details from filename {filename}: {e}")
        return None, None

def bulk_import_forecast_data(forecast_data):
    try:
        # Step 1: Build a set of unique keys from forecast_data
        unique_keys = set(
            (data['place'].id, data['date'], data['hour'], data['utc_cycle_time'])
            for data in forecast_data
        )

        # Step 2: Fetch existing records matching these keys
        existing_records = GFSForecast.objects.filter(
            place__in=[data['place'] for data in forecast_data],
            date__in=[data['date'] for data in forecast_data],
            hour__in=[data['hour'] for data in forecast_data],
            utc_cycle_time__in=[data['utc_cycle_time'] for data in forecast_data]
        )

        existing_keys = set(
            (record.place.id, record.date, record.hour, record.utc_cycle_time)
            for record in existing_records
        )

        # Step 3: Separate new records and records to update
        new_records = []
        records_to_update = []

        # Create a mapping for existing records to update
        existing_records_dict = {
            (record.place.id, record.date, record.hour, record.utc_cycle_time): record
            for record in existing_records
        }

        for data in forecast_data:
            key = (data['place'].id, data['date'], data['hour'], data['utc_cycle_time'])
            if key in existing_keys:
                # Update existing record
                record = existing_records_dict[key]
                record.latitude = data['latitude']
                record.longitude = data['longitude']
                # Update forecast_data dictionary
                record.forecast_data.update(data['forecast_data'])
                records_to_update.append(record)
            else:
                # Create new record
                new_records.append(GFSForecast(
                    place=data['place'],
                    latitude=data['latitude'],
                    longitude=data['longitude'],
                    date=data['date'],
                    hour=data['hour'],
                    utc_cycle_time=data['utc_cycle_time'],
                    forecast_data=data['forecast_data']
                ))

        # Step 4: Bulk create new records
        if new_records:
            GFSForecast.objects.bulk_create(new_records, batch_size=1000, ignore_conflicts=True)
            logger.info("Bulk inserted %d new records", len(new_records))

        # Step 5: Bulk update existing records
        if records_to_update:
            GFSForecast.objects.bulk_update(
                records_to_update,
                fields=['latitude', 'longitude', 'forecast_data'],
                batch_size=1000
            )
            logger.info("Bulk updated %d existing records", len(records_to_update))

        total_records = len(new_records) + len(records_to_update)
        logger.info("Processed %d records (%d new, %d updated)", total_records, len(new_records), len(records_to_update))

    except Exception as e:
        logger.error(f"Error during bulk import: {e}")

def process_grib_message(grib, valid_datetime, utc_cycle_time, places):
    forecast_data = []
    data = grib.values
    lats, lons = grib.latlons()

    param_name = f"{grib.shortName.lower()}_level_{grib.level}_{grib.typeOfLevel}"

    # Flatten lats and lons to 1D arrays
    latitudes = lats.flatten()
    longitudes = lons.flatten()

    # Create a KDTree for efficient nearest neighbor search
    grid_points = np.column_stack((latitudes, longitudes))
    grid_tree = cKDTree(grid_points)

    # Prepare arrays of place coordinates
    place_coords = []
    place_list = []
    for place in places:
        place_coords.append((place.location.y, place.location.x))  # (latitude, longitude)
        place_list.append(place)

    place_coords = np.array(place_coords)

    # Query the KDTree to find nearest grid point for each place
    distances, indices = grid_tree.query(place_coords, k=1)

    # Extract the data values at those indices
    data_flat = data.flatten()
    for i, index in enumerate(indices):
        value = data_flat[index]
        if isinstance(value, np.ma.core.MaskedConstant):
            value = None
        else:
            value = float(value)

        forecast_entry = {
            'place': place_list[i],
            'latitude': place_coords[i][0],
            'longitude': place_coords[i][1],
            'forecast_data': {param_name: value},
            'date': valid_datetime.date(),
            'hour': valid_datetime.hour,
            'utc_cycle_time': utc_cycle_time,
        }

        forecast_data.append(forecast_entry)

    # Bulk insert or update the forecast data
    bulk_import_forecast_data(forecast_data)

def parse_and_import_gfs_data(file_path):
    logger.info("Starting to parse GFS data from %s.", file_path)

    valid_datetime, utc_cycle_time = extract_forecast_details_from_filename(file_path)
    if valid_datetime is None or utc_cycle_time is None:
        logger.error("Could not extract datetime details from filename: %s", file_path)
        return

    try:
        # Retrieve all places from the database
        places = list(GeographicPlace.objects.all())
        if not places:
            logger.error("No places found in the database.")
            return

        with pygrib.open(file_path) as gribs:
            total_messages = gribs.messages
            logger.info("Total number of messages in the GRIB file: %d", total_messages)

            for i, grib in enumerate(gribs, start=1):
                logger.info(
                    "Processing message %d of %d. Parameter: %s, Level: %d, Type of Level: %s",
                    i, total_messages, grib.parameterName, grib.level, grib.typeOfLevel
                )
                logger.info("Valid datetime is %s (UTC)", valid_datetime.isoformat())

                process_grib_message(grib, valid_datetime, utc_cycle_time, places)

    except Exception as e:
        logger.error("Error processing GRIB file %s: %s", file_path, e)

    logger.info("Finished parsing GFS data from %s.", file_path)

    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info("Deleted GRIB file: %s", file_path)

class Command(BaseCommand):
    help = 'Import GFS data into the database'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='Path to the filtered GRIB2 file')

    def handle(self, *args, **options):
        logger.info("Starting the GFS data import process.")

        file_path = options['file']
        if file_path:
            logger.info(f"File path provided: {file_path}")
            parse_and_import_gfs_data(file_path)
        else:
            filtered_directory = 'data/filtered_data'
            logger.info(f"Looking for files in: {filtered_directory}")
            if not os.path.exists(filtered_directory):
                logger.error(f"Filtered directory not found: {filtered_directory}")
                return

            total_files = 0
            for root, dirs, files in os.walk(filtered_directory):
                for file in files:
                    if file.endswith('.grib2'):
                        total_files += 1
                        file_path = os.path.join(root, file)
                        logger.info(f"Found GRIB file: {file_path}")
                        try:
                            parse_and_import_gfs_data(file_path)
                        except Exception as e:
                            logger.error("Error processing file %s: %s", file_path, e)

            logger.info(f"Total GRIB files processed: {total_files}")

        logger.info("GFS data import process completed for all files.")
