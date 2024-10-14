import os
import logging
import shutil
from datetime import datetime, timedelta, timezone
from django.core.management.base import BaseCommand

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

data_directory = "data"
combined_directory = os.path.join(data_directory, "combined_data")

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

def cleanup_old_gfs_data():
    latest_cycles = get_latest_cycles(count=2)  # Keep only the latest 2 cycles
    latest_cycle_folders = {f"{date}_{hour}" for date, hour in latest_cycles}

    # Clean up old GFS data folders
    for folder_name in os.listdir(data_directory):
        folder_path = os.path.join(data_directory, folder_name)
        if os.path.isdir(folder_path) and folder_name not in latest_cycle_folders and folder_name != "combined_data":
            shutil.rmtree(folder_path)
            logger.info("Deleted old folder: %s", folder_path)

    # Clean up old combined data files
    if os.path.exists(combined_directory):
        for file_name in os.listdir(combined_directory):
            if file_name.startswith("combined_"):
                combined_cycle = file_name.split("_")[1] + "_" + file_name.split("_")[2].split(".")[0]
                if combined_cycle not in latest_cycle_folders:
                    file_path = os.path.join(combined_directory, file_name)
                    os.remove(file_path)
                    logger.info("Deleted old combined file: %s", file_path)

class Command(BaseCommand):
    help = 'Clean up old GFS data and combined data folders'

    def handle(self, *args, **kwargs):
        logger.info("Starting cleanup of old GFS data and combined data folders.")
        cleanup_old_gfs_data()
        logger.info("Cleanup of old GFS data and combined data folders completed.")