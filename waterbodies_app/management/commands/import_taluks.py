# waterbodies_app/management/commands/import_taluks.py

import pandas as pd
from django.core.management.base import BaseCommand
from waterbodies_app.models import Taluk  # Adjust the import path as needed

class Command(BaseCommand):
    help = 'Import taluks from an Excel file'

    def handle(self, *args, **options):
        excel_file_path = 'C:\\waterbodies_project\\waterBodyAdmin_taluk.xlsx'  # Replace with the actual path of your Excel file

        # Clear existing records
        Taluk.objects.all().delete()

        try:
            # Read the Excel file
            taluks_data = pd.read_excel(excel_file_path)

            # Iterate over the rows in the Excel file and create Taluk instances
            for _, row in taluks_data.iterrows():
                Taluk.objects.create(
                    code=row['code'],  # Adjust these column names to match your Excel file
                    name=row['name'],
                    district_id=row['district_id']  # No need for ForeignKey; treated as a simple field
                )

            self.stdout.write(self.style.SUCCESS('Taluks imported successfully!'))
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.WARNING('The Excel file is empty.'))
        except pd.errors.ParserError as e:
            self.stdout.write(self.style.ERROR(f'Error parsing Excel file: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))
