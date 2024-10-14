import os
import logging
import pygrib
from django.core.management.base import BaseCommand
from django.utils import timezone
from weather_engine.models import GFSParameter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_and_import_gfs_parameters(file_path):
    parameters = []
    try:
        with pygrib.open(file_path) as gribs:
            for grib in gribs:
                try:
                    param_number = grib['parameterNumber']
                    parameter_category = grib['parameterCategory']
                    level_layer = grib['level']
                    short_name = grib['shortName']
                    parameter = grib['parameterName']  # Adjusted to use 'parameterName' if available
                    forecast_valid = grib['typeOfLevel']
                    description = grib['name']
                    parameters.append({
                        "number": param_number,
                        "parameter_category": parameter_category,
                        "level_layer": level_layer,
                        "short_name": short_name,
                        "parameter": parameter,
                        "forecast_valid": forecast_valid,
                        "description": description,
                        "enabled": True  # Default to enabled; adjust as needed
                    })
                except KeyError as e:
                    logger.error(f"KeyError while reading GRIB message: {e}")
    except Exception as e:
        logger.error(f"Error reading GRIB2 file: {e}")

    logger.info(f"Fetched and parsed {len(parameters)} GFS parameters from the file.")

    # Import parameters directly into the database
    import_parameters_to_db(parameters)

def import_parameters_to_db(parameters):
    for param in parameters:
        try:
            GFSParameter.objects.update_or_create(
                number=param["number"],
                level_layer=str(param["level_layer"]),
                parameter=param["parameter"],
                defaults={
                    'parameter_category': param["parameter_category"],
                    'short_name': param["short_name"],
                    'forecast_valid': param["forecast_valid"],
                    'description': param["description"],
                    'enabled': param["enabled"],
                    'last_updated': timezone.now(),
                }
            )
            logger.info(f"Imported parameter: {param['parameter']} (Number: {param['number']}, Level: {param['level_layer']})")
        except Exception as e:
            logger.error(f"Error importing parameter {param['parameter']}: {e}")

class Command(BaseCommand):
    help = 'Extract GFS parameters from a GRIB file and import them into the database'

    def handle(self, *args, **options):
        logger.info("Starting the GFS parameter extraction and import process from GRIB2 file.")

        input_file = "data/control.grib2"

        if not os.path.exists(input_file):
            logger.error(f"Input file not found: {input_file}")
            return

        extract_and_import_gfs_parameters(input_file)
        logger.info("GFS parameter extraction and import process completed.")
