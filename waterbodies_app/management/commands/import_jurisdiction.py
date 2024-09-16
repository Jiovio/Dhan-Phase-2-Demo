# waterbodies_app/management/commands/import_jurisdictions.py

import pandas as pd
from django.core.management.base import BaseCommand
from waterbodies_app.models import Jurisdiction  # Adjust the import path as needed

class Command(BaseCommand):
    help = 'Import jurisdictions from an Excel file'

    def handle(self, *args, **options):
        excel_file_path = 'C:\\waterbodies_project\\waterBodyAdmin_jurisdiction.xlsx'  # Replace with the actual path of your Excel file

        # Clear existing records
        Jurisdiction.objects.all().delete()

        try:
            # Read the Excel file
            jurisdictions_data = pd.read_excel(excel_file_path)

            # Iterate over the rows in the Excel file and create Jurisdiction instances
            for _, row in jurisdictions_data.iterrows():
                Jurisdiction.objects.create(
                    code=row['code'],  # Adjust these column names to match your Excel file
                    createdBy=row['createdBy']  # Ensure this matches your Excel file's column name
                )

            self.stdout.write(self.style.SUCCESS('Jurisdictions imported successfully!'))
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.WARNING('The Excel file is empty.'))
        except pd.errors.ParserError as e:
            self.stdout.write(self.style.ERROR(f'Error parsing Excel file: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))
