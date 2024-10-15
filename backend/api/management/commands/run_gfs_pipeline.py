import logging
from django.core.management.base import BaseCommand
from django.core.management import call_command

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Run the GFS data processing pipeline'

    def handle(self, *args, **options):
        logger.info("Starting GFS data processing pipeline.")

        commands = [
            'gfs_data_download',
            'gfs_data_filtered',
            'gfs_data_import',
            'gfs_data_cleanup',
        ]

        for command in commands:
            logger.info(f"Running command: {command}")
            call_command(command)

        logger.info("GFS data processing pipeline completed.")
