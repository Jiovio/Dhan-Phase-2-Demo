import pandas as pd
from django.core.management.base import BaseCommand
from waterbodies_app.models import Availability  # Adjust the import path as needed

class Command(BaseCommand):
    help = 'Import availability data from an Excel file'

    def handle(self, *args, **options):
        excel_file_path = 'C:\\waterbodies_project\\waterbodyavailability.xlsx'  # Replace with the actual path of your Excel file

        # Clear existing records
        Availability.objects.all().delete()

        try:
            # Read the Excel file
            availability_data = pd.read_excel(excel_file_path)

            # Iterate over the rows in the Excel file and create Availability instances
            for _, row in availability_data.iterrows():
                Availability.objects.create(
                    name=row['name']  # Adjust column name to match your Excel file
                )

            self.stdout.write(self.style.SUCCESS('Availability data imported successfully!'))
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.WARNING('The Excel file is empty.'))
        except pd.errors.ParserError as e:
            self.stdout.write(self.style.ERROR(f'Error parsing Excel file: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))
