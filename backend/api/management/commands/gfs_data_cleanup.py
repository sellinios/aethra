import os
import logging
import shutil
from datetime import datetime, timedelta, timezone
from django.core.management.base import BaseCommand
from weather.models.model_gfs_forecast import GFSForecast

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Define the data directories
DATA_DIRECTORY = "data"
COMBINED_DIRECTORY = os.path.join(DATA_DIRECTORY, "combined_data")

def delete_tmp_files():
    for root, dirs, files in os.walk(DATA_DIRECTORY):
        for file in files:
            if file.endswith('.tmp'):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    logger.info(f"Deleted temporary file: {file_path}")
                except Exception as e:
                    logger.error(f"Failed to delete {file_path}: {e}")

def cleanup_old_gfs_data():
    # Number of days to keep
    days_to_keep = 2

    # Get the current date in UTC
    current_date = datetime.utcnow().date()
    cutoff_date = current_date - timedelta(days=days_to_keep - 1)
    logger.info(f"Deleting GFS data folders with date before {cutoff_date}")

    # List all data folders excluding 'combined_data'
    data_folders = [f for f in os.listdir(DATA_DIRECTORY)
                    if os.path.isdir(os.path.join(DATA_DIRECTORY, f)) and f != "combined_data"]

    for folder_name in data_folders:
        parts = folder_name.split('_')
        if len(parts) >= 2:
            date_str = parts[0]
            try:
                folder_date = datetime.strptime(date_str, "%Y%m%d").date()
                if folder_date < cutoff_date:
                    folder_path = os.path.join(DATA_DIRECTORY, folder_name)
                    try:
                        shutil.rmtree(folder_path)
                        logger.info(f"Deleted old folder: {folder_path}")
                    except Exception as e:
                        logger.error(f"Failed to delete folder {folder_path}: {e}")
            except ValueError:
                continue

    # Clean up old combined data files
    if os.path.exists(COMBINED_DIRECTORY):
        for file_name in os.listdir(COMBINED_DIRECTORY):
            if file_name.startswith("combined_"):
                parts = file_name.split("_")
                if len(parts) >= 3:
                    date_str = parts[1]
                    try:
                        file_date = datetime.strptime(date_str, "%Y%m%d").date()
                        if file_date < cutoff_date:
                            file_path = os.path.join(COMBINED_DIRECTORY, file_name)
                            try:
                                os.remove(file_path)
                                logger.info(f"Deleted old combined file: {file_path}")
                            except Exception as e:
                                logger.error(f"Failed to delete combined file {file_path}: {e}")
                    except ValueError:
                        continue

def delete_old_gfs_forecast_entries():
    # Number of days to keep
    days_to_keep = 2

    # Get the current date in UTC
    current_date = datetime.utcnow().date()
    cutoff_date = current_date - timedelta(days=days_to_keep - 1)
    logger.info(f"Deleting GFSForecast data with date before {cutoff_date}")

    # Delete entries older than the cutoff date
    num_deleted, _ = GFSForecast.objects.filter(date__lt=cutoff_date).delete()
    logger.info(f"Deleted {num_deleted} old GFSForecast entries with date before {cutoff_date}")

def cleanup_data():
    logger.info("Starting cleanup of data.")

    # Step 1: Delete .tmp files
    logger.info("Deleting temporary files.")
    delete_tmp_files()

    # Step 2: Clean up old GFS data folders and files
    logger.info("Cleaning up old GFS data folders and files.")
    cleanup_old_gfs_data()

    # Step 3: Delete old GFSForecast entries from the database
    logger.info("Deleting old GFSForecast entries from the database.")
    delete_old_gfs_forecast_entries()

    logger.info("Cleanup of data completed.")

class Command(BaseCommand):
    help = 'Clean up old GFS data, delete .tmp files, and remove old database entries'

    def handle(self, *args, **kwargs):
        cleanup_data()
