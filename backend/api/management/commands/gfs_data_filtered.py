import os
import logging
import pygrib
from datetime import datetime, timezone, timedelta
from django.core.management.base import BaseCommand
from weather_engine.models import GFSParameter

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def extract_forecast_details(filename, folder_name):
    try:
        # Example filename: gfs.t12z.pgrb2.0p25.f000
        parts = filename.split('.')
        cycle_hour = parts[1][1:3]  # Extract '12' from 't12z'
        forecast_hour_str = parts[-1][1:]  # Extract '000' from 'f000'

        # Use folder name as date string (assuming it is 'YYYYMMDD_HH')
        date_str = folder_name.split('_')[0]  # Extract '20241018'

        cycle_datetime = datetime.strptime(f"{date_str}{cycle_hour}", "%Y%m%d%H").replace(tzinfo=timezone.utc)
        forecast_hour = int(forecast_hour_str)
        valid_datetime = cycle_datetime + timedelta(hours=forecast_hour)

        return valid_datetime, cycle_datetime, forecast_hour
    except Exception as e:
        logger.error(f"Error extracting details from filename {filename}: {e}")
        return None, None, None

def list_available_parameters(file_path):
    parameters = set()
    try:
        with pygrib.open(file_path) as gribs:
            for grib in gribs:
                param_key = (grib.parameterCategory, grib.level, grib.shortName, grib.name)
                parameters.add(param_key)
    except Exception as e:
        logger.error(f"Error listing parameters in GRIB file {file_path}: {e}")
    return parameters

def standardize_param_key(param):
    """Standardize the parameter key for consistent comparison."""
    return (
        int(param[0]),               # parameterCategory
        int(param[1]),               # level
        str(param[2]).lower(),       # shortName
        str(param[3]).lower()        # name
    )

def filter_grib_messages(file_path, relevant_parameters, new_file_path):
    try:
        with pygrib.open(file_path) as gribs, open(new_file_path, 'wb') as new_grib_file:
            messages_written = 0
            for grib in gribs:
                param_key = standardize_param_key((
                    grib.parameterCategory,
                    grib.level,
                    grib.shortName,
                    grib.name
                ))
                if param_key in relevant_parameters:
                    new_grib_file.write(grib.tostring())
                    messages_written += 1
            if messages_written > 0:
                logger.info(f"Saved {messages_written} messages to {new_file_path}")
            else:
                logger.warning(f"No matching parameters found in {file_path}")
    except Exception as e:
        logger.error(f"Error while filtering GRIB file {file_path}: {e}")

class Command(BaseCommand):
    """
    Filter and save GRIB data based on enabled parameters in the database.
    """

    help = 'Filter and save GRIB data based on enabled parameters in the database'

    def handle(self, *args, **options):
        logger.info("Starting the GRIB data filtering process.")

        base_directory = "data"
        filtered_directory = os.path.join(base_directory, "filtered_data")
        os.makedirs(filtered_directory, exist_ok=True)

        # Collect all GRIB files in subdirectories starting with date
        grib_files = []
        for subdir in os.listdir(base_directory):
            subdir_path = os.path.join(base_directory, subdir)
            if os.path.isdir(subdir_path) and subdir.startswith("2024"):
                for filename in os.listdir(subdir_path):
                    if filename.startswith('gfs') and '.f' in filename:
                        grib_files.append((subdir, filename))

        if not grib_files:
            logger.error("No GRIB files found in data directories.")
            return

        try:
            # Build a set of enabled parameters
            relevant_parameters = {
                standardize_param_key((
                    param.parameter_category,
                    param.level_layer,
                    param.short_name,
                    param.description
                ))
                for param in GFSParameter.objects.filter(enabled=True)
            }
            if not relevant_parameters:
                logger.warning("No enabled parameters found.")
                return

            logger.info(f"Enabled parameters: {relevant_parameters}")

            for folder_name, filename in grib_files:
                file_path = os.path.join(base_directory, folder_name, filename)
                valid_datetime, cycle_datetime, forecast_hour = extract_forecast_details(filename, folder_name)
                if valid_datetime is None:
                    logger.error(f"Skipping file due to error in extracting details: {file_path}")
                    continue

                # Create output subdirectory for the cycle
                filtered_subdirectory = os.path.join(filtered_directory, folder_name)
                os.makedirs(filtered_subdirectory, exist_ok=True)

                # Name the filtered file
                new_file_name = f"filtered_{valid_datetime.strftime('%Y%m%d_%H%M')}_f{forecast_hour:03d}.grib2"
                new_file_path = os.path.join(filtered_subdirectory, new_file_name)

                # Check available parameters in the GRIB file
                available_parameters = list_available_parameters(file_path)
                standardized_available_parameters = {standardize_param_key(param) for param in available_parameters}

                # Find matching parameters
                matching_parameters = relevant_parameters & standardized_available_parameters

                if matching_parameters:
                    logger.info(f"Filtering data from {file_path} to {new_file_path}")
                    filter_grib_messages(file_path, matching_parameters, new_file_path)
                else:
                    logger.warning(f"No relevant parameters found in {file_path}. Skipping file.")

            logger.info("GRIB data filtering process completed.")

        except Exception as e:
            logger.error(f"Error during the filtering process: {e}")
