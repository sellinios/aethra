from datetime import datetime, timedelta, timezone
import logging
import os
import requests
from django.core.management.base import BaseCommand

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_gfs_data_sequence(base_url, date, hour, forecast_hours, save_directory, dry_run=False):
    os.makedirs(save_directory, exist_ok=True)
    grib_files = []

    for forecast_hour in forecast_hours:
        file_name = f"gfs.t{hour}z.pgrb2.0p25.f{forecast_hour:03}"
        url = f"{base_url}/gfs.{date}/{hour}/atmos/{file_name}"
        temp_save_path = os.path.join(save_directory, f"gfs_{date}_{hour}_{forecast_hour:03}.grib2.tmp")
        final_save_path = os.path.join(save_directory, f"gfs_{date}_{hour}_{forecast_hour:03}.grib2")

        if not os.path.exists(final_save_path):
            if not dry_run:
                response = requests.get(url, stream=True, timeout=60)
                if response.status_code == 200:
                    with open(temp_save_path, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                file.write(chunk)
                    os.rename(temp_save_path, final_save_path)
                    logger.info("Downloaded GFS data to %s", final_save_path)
                    grib_files.append(final_save_path)
                else:
                    logger.warning("Failed to download GFS data from %s", url)
                    if os.path.exists(temp_save_path):
                        os.remove(temp_save_path)
            else:
                logger.info(f"DRY RUN: Would download {url} to {final_save_path}")
                grib_files.append(final_save_path)
        else:
            logger.info("File already exists: %s", final_save_path)
            grib_files.append(final_save_path)
    return grib_files

def is_directory_complete(directory, expected_file_count):
    if not os.path.exists(directory):
        return False
    return len(os.listdir(directory)) >= expected_file_count

def get_latest_cycles(count=2):
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    cycles = ['00', '06', '12', '18']
    latest_cycles = []

    for i in range(24):  # Check the last 24 hours
        cycle_time = now - timedelta(hours=i)
        date = cycle_time.strftime("%Y%m%d")
        hour = cycle_time.strftime("%H")
        if hour in cycles and (date, hour) not in latest_cycles:
            latest_cycles.append((date, hour))
        if len(latest_cycles) == count:
            break

    return latest_cycles

class Command(BaseCommand):
    help = 'Download GFS data into the specified folders'

    def add_arguments(self, parser):
        parser.add_argument('--base_url', type=str, default="https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod")
        parser.add_argument('--max_hours', type=int, default=120, help='Maximum number of forecast hours to download')
        parser.add_argument('--dry_run', action='store_true', help='Run the script without actually downloading files')

    def handle(self, *args, **options):
        logger.info("Starting the GFS data download process.")

        base_url = options['base_url']
        max_hours = options['max_hours']  # Get the maximum number of hours to download from arguments
        dry_run = options['dry_run']

        latest_cycles = get_latest_cycles(count=2)  # Change from 4 to 2
        expected_file_count = min(max_hours, len(set(range(121)) | set(range(13, 385))))

        # Adjust forecast hours based on the max_hours input
        if max_hours > 120:
            forecast_hours_0_120 = list(range(0, 121, 1))
            forecast_hours_120_384 = list(range(123, min(385, max_hours + 1), 3))
            forecast_hours = forecast_hours_0_120 + forecast_hours_120_384
        else:
            forecast_hours = list(range(0, max_hours + 1, 1))

        logger.info(f"Forecast hours (max {max_hours} hours): {forecast_hours}")

        for date, hour in latest_cycles:
            save_directory = f"data/{date}_{hour}"
            if is_directory_complete(save_directory, expected_file_count):
                logger.info("Directory already exists and is complete: %s, skipping download.", save_directory)
                continue
            logger.info("Attempting to download data for date: %s, hour: %s", date, hour)
            grib_files = download_gfs_data_sequence(base_url, date, hour, forecast_hours, save_directory, dry_run)
            if grib_files:
                logger.info("Successfully downloaded data for date: %s, hour: %s", date, hour)
            else:
                logger.warning("Failed to download data for date: %s, hour: %s", date, hour)

        logger.info("GFS data download process completed for the latest 2 cycles.")
