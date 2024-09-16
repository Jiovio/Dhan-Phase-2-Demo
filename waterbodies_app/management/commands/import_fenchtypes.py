# waterbodies_app/management/commands/import_fencetypes.py

import pandas as pd
from django.core.management.base import BaseCommand
from waterbodies_app.models import FenceType  # Adjust the import path as needed

class Command(BaseCommand):
    help = 'Import FenceTypes from an Excel file'

    def handle(self, *args, **options):
        excel_file_path = 'C:\\waterbodies_project\\waterBodyAdmin_waterbodyfencetype.xlsx'  # Replace with the actual path of your Excel file

        # Clear existing records to avoid duplicates
        FenceType.objects.all().delete()

        try:
            # Read the Excel file
            fencetypes_data = pd.read_excel(excel_file_path)

            # Check if the necessary column 'name' is in the dataframe
            if 'name' not in fencetypes_data.columns:
                self.stdout.write(self.style.ERROR('The Excel file does not contain a "name" column.'))
                return

            # Iterate over the rows in the Excel file and create FenceType instances
            for _, row in fencetypes_data.iterrows():
                FenceType.objects.create(
                    name=row['name']  # Adjust this if your Excel file uses different column names
                )

            self.stdout.write(self.style.SUCCESS('FenceTypes imported successfully!'))

        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.WARNING('The Excel file is empty.'))
        except pd.errors.ParserError as e:
            self.stdout.write(self.style.ERROR(f'Error parsing Excel file: {e}'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('The specified Excel file does not exist.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))
