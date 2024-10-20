import geopandas as gpd
import requests
import zipfile
import os
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from geography.models import GeographicData

class Command(BaseCommand):
    help = 'Load geographic data (municipalities) from GeoJSON files into the database'

    def handle(self, *args, **kwargs):
        files_info = [
            {"url": "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_GRC_3.json.zip", "file": "gadm41_GRC_3.json"},
        ]
        extract_path = "data/"

        # Ensure the data directory exists
        if not os.path.exists(extract_path):
            os.makedirs(extract_path)
            self.stdout.write(self.style.SUCCESS(f'Created directory: {extract_path}'))

        for file_info in files_info:
            zip_url = file_info['url']
            zip_path = os.path.join(extract_path, os.path.basename(zip_url))

            try:
                # Download the zip file
                self.stdout.write(self.style.SUCCESS(f"Downloading {zip_url}..."))
                response = requests.get(zip_url)
                response.raise_for_status()  # Ensure we catch any errors in the download process

                with open(zip_path, 'wb') as file:
                    file.write(response.content)

                # Unzip the file
                self.stdout.write(self.style.SUCCESS(f"Unzipping {zip_path}..."))
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)

                # Load the GeoJSON file
                geojson_file = os.path.join(extract_path, file_info['file'])
                self.stdout.write(self.style.SUCCESS(f"Loading data from {geojson_file}..."))
                gdf = gpd.read_file(geojson_file)

                # Print column names to understand the structure
                self.stdout.write(self.style.SUCCESS(f"Columns: {gdf.columns}"))

                # Create and save the GeographicData instances (focus on municipalities)
                for index, row in gdf.iterrows():
                    # Check for columns corresponding to municipality information
                    if 'NAME_3' in row and 'GID_3' in row:
                        name = row['NAME_3']
                        gid = row['GID_3']
                    elif 'NAME_2' in row and 'GID_2' in row:
                        # Fallback to Level 2 if Level 3 info is not available
                        name = row['NAME_2']
                        gid = row['GID_2']
                    else:
                        self.stdout.write(self.style.ERROR(f"Skipping row {index}, no suitable municipality info found."))
                        continue

                    geometry = row['geometry']

                    # Convert the Shapely geometry to a GEOSGeometry
                    geos_geometry = GEOSGeometry(geometry.wkt, srid=4326)

                    # Create and save the GeographicData instance
                    geo_data = GeographicData(gid=gid, name=name, geometry=geos_geometry)
                    geo_data.save()

                self.stdout.write(self.style.SUCCESS(f"Data from {geojson_file} loaded successfully!"))

            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Error downloading {zip_url}: {e}"))
            except zipfile.BadZipFile as e:
                self.stdout.write(self.style.ERROR(f"Error unzipping {zip_path}: {e}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing {geojson_file}: {e}"))

        self.stdout.write(self.style.SUCCESS("All geographic data loaded successfully!"))
