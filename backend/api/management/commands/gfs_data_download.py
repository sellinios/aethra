from datetime import datetime, timedelta, timezone
import logging
import os
import requests
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_available_files(base_url, date, hour):
    """
    Retrieves the list of available files on the NOAA server for a given cycle.

    Args:
        base_url (str): Base URL of the NOAA server.
        date (str): Date in YYYYMMDD format.
        hour (str): Hour in HH format.

    Returns:
        set: A set containing the names of available files.
    """
    cycle_url = f"{base_url}/gfs.{date}/{hour}/atmos/"
    try:
        response = requests.get(cycle_url, timeout=60)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            files = set()
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and 'grb2' in href:
                    files.add(href.strip())
            return files
        else:
            logger.warning("Failed to access %s (Status Code: %d)", cycle_url, response.status_code)
            return set()
    except requests.RequestException as e:
        logger.warning("Error accessing %s: %s", cycle_url, e)
        return set()

def find_latest_complete_cycle(base_url, forecast_hours, max_cycles=10):
    """
    Finds the latest cycle that has all required files available on the NOAA server.

    Args:
        base_url (str): Base URL of the NOAA server.
        forecast_hours (list): List of forecast hours to check.
        max_cycles (int): Maximum number of past cycles to check.

    Returns:
        tuple or None: (date, hour) of the latest complete cycle, or None if not found.
    """
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    cycles = ['00', '06', '12', '18']
    expected_files = set(f"gfs.t{hour}z.pgrb2.0p25.f{fhour:03}" for fhour in forecast_hours for hour in cycles)

    for i in range(max_cycles * 6):  # Check up to max_cycles cycles back
        cycle_time = now - timedelta(hours=i)
        hour = cycle_time.strftime("%H")
        if hour not in cycles:
            continue
        date = cycle_time.strftime("%Y%m%d")
        logger.info("Checking availability for cycle Date=%s, Hour=%s", date, hour)
        available_files = get_available_files(base_url, date, hour)
        expected_files_for_cycle = set(f"gfs.t{hour}z.pgrb2.0p25.f{fhour:03}" for fhour in forecast_hours)
        if expected_files_for_cycle.issubset(available_files):
            logger.info("All required files are available for cycle Date=%s, Hour=%s", date, hour)
            return date, hour
        else:
            logger.info("Not all required files are available for cycle Date=%s, Hour=%s", date, hour)
    logger.warning("No complete cycles found in the last %d cycles.", max_cycles)
    return None, None

def download_gfs_data_sequence(base_url, date, hour, forecast_hours, save_directory, dry_run=False):
    """
    Downloads a sequence of GFS data files for specified forecast hours.

    Args:
        base_url (str): Base URL from where to download the data.
        date (str): Date in YYYYMMDD format.
        hour (str): Hour in HH format.
        forecast_hours (list): List of forecast hours to download.
        save_directory (str): Directory to save the downloaded files.
        dry_run (bool): If True, simulates the download without saving files.

    Returns:
        list: List of paths to the downloaded (or expected) GRIB2 files.
    """
    os.makedirs(save_directory, exist_ok=True)
    grib_files = []

    for forecast_hour in forecast_hours:
        file_name = f"gfs.t{hour}z.pgrb2.0p25.f{forecast_hour:03}"
        url = f"{base_url}/gfs.{date}/{hour}/atmos/{file_name}"
        temp_save_path = os.path.join(save_directory, f"{file_name}.tmp")
        final_save_path = os.path.join(save_directory, f"{file_name}")

        if not os.path.exists(final_save_path):
            if not dry_run:
                try:
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
                        logger.warning("Failed to download GFS data from %s (Status Code: %d)", url, response.status_code)
                        if os.path.exists(temp_save_path):
                            os.remove(temp_save_path)
                except requests.RequestException as e:
                    logger.warning("Error downloading %s: %s", url, e)
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
    """
    Checks if the specified directory contains at least the expected number of files.

    Args:
        directory (str): Path to the directory.
        expected_file_count (int): The expected number of files.

    Returns:
        bool: True if directory exists and contains >= expected_file_count files, else False.
    """
    if not os.path.exists(directory):
        return False
    actual_file_count = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
    return actual_file_count >= expected_file_count

class Command(BaseCommand):
    help = 'Download GFS data into the specified folders'

    def add_arguments(self, parser):
        parser.add_argument(
            '--base_url',
            type=str,
            default="https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod",
            help='Base URL for GFS data download'
        )
        parser.add_argument(
            '--max_hours',
            type=int,
            default=385,
            help='Maximum number of forecast hours to download (default: 385)'
        )
        parser.add_argument(
            '--dry_run',
            action='store_true',
            help='Run the script without actually downloading files'
        )
        parser.add_argument(
            '--max_cycles',
            type=int,
            default=10,
            help='Maximum number of past cycles to check (default: 10)'
        )

    def handle(self, *args, **options):
        """
        Main entry point for the management command.
        """
        logger.info("Starting the GFS data download process.")

        base_url = options['base_url']
        max_hours = options['max_hours']
        dry_run = options['dry_run']
        max_cycles = options['max_cycles']

        # Define forecast_hours based on max_hours
        if max_hours > 120:
            forecast_hours_0_120 = list(range(0, 121, 1))
            # Forecast hours after 120 are typically in 3-hour increments
            forecast_hours_120_plus = list(range(123, min(385, max_hours + 1), 3))
            forecast_hours = forecast_hours_0_120 + forecast_hours_120_plus
        else:
            forecast_hours = list(range(0, max_hours + 1, 1))

        expected_file_count = len(forecast_hours)
        logger.info(f"Forecast hours (max {max_hours} hours): {forecast_hours}")
        logger.info(f"Expected number of files per cycle: {expected_file_count}")

        # Find the latest complete cycle
        date, hour = find_latest_complete_cycle(base_url, forecast_hours, max_cycles)
        if date is None or hour is None:
            logger.error("No complete cycles found. Exiting.")
            return

        save_directory = os.path.join("data", f"{date}_{hour}")
        logger.info("Processing cycle: Date=%s, Hour=%s", date, hour)

        if is_directory_complete(save_directory, expected_file_count):
            logger.info("Directory already exists and is complete: %s, skipping download.", save_directory)
        else:
            logger.info("Attempting to download data for date: %s, hour: %s", date, hour)
            grib_files = download_gfs_data_sequence(
                base_url=base_url,
                date=date,
                hour=hour,
                forecast_hours=forecast_hours,
                save_directory=save_directory,
                dry_run=dry_run
            )

            if len(grib_files) >= expected_file_count:
                logger.info("Successfully downloaded data for date: %s, hour: %s", date, hour)
            else:
                logger.warning("Failed to download all data for date: %s, hour: %s", date, hour)

        logger.info("GFS data download process completed.")
