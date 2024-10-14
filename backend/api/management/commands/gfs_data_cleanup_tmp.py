import os
import logging
from django.core.management.base import BaseCommand

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

data_directory = "data"

def delete_tmp_files():
    for root, dirs, files in os.walk(data_directory):
        for file in files:
            if file.endswith('.tmp'):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    logger.info(f"Deleted temporary file: {file_path}")
                except Exception as e:
                    logger.error(f"Failed to delete {file_path}: {e}")

class Command(BaseCommand):
    help = 'Delete .tmp files in the data directory and its subdirectories'

    def handle(self, *args, **kwargs):
        logger.info("Starting deletion of .tmp files.")
        delete_tmp_files()
        logger.info("Deletion of .tmp files completed.")