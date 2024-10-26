import pandas as pd
from django.core.management.base import BaseCommand
from waterbodies_app.models import Cropings  # Adjust the import path as needed

class Command(BaseCommand):
    help = 'Import cropings from an Excel file'

    def handle(self, *args, **options):
        excel_file_path = 'C:\\waterdams_project\\croppings.xlsx'  # Adjust the path

        # Clear existing records if needed
        Cropings.objects.all().delete()

        try:
            # Read the Excel file
            cropings_data = pd.read_excel(excel_file_path)

            # Iterate over the rows in the Excel file and create Cropings instances
            for _, row in cropings_data.iterrows():
                Cropings.objects.create(
                    name=row['name']  # Adjust 'name' if different in Excel
                )

            self.stdout.write(self.style.SUCCESS('Cropings imported successfully!'))
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.WARNING('The Excel file is empty.'))
        except pd.errors.ParserError as e:
            self.stdout.write(self.style.ERROR(f'Error parsing Excel file: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))
