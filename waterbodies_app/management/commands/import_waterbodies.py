# waterbodies/management/commands/import_waterbodies.py
import pandas as pd
from django.core.management.base import BaseCommand
from waterbodies_app.models import WaterBody  # Import your WaterBody model here

class Command(BaseCommand):
    help = 'Import water bodies from Excel file'

    def handle(self, *args, **options):
        excel_file_path = 'C:\\waterbodies_project\\wb.xlsx'  # Replace with the actual path of your Excel file

        # Clear existing records
        WaterBody.objects.all().delete()

        try:
            waterbodies_data = pd.read_excel(excel_file_path)

            for _, row in waterbodies_data.iterrows():
                WaterBody.objects.create(
                    Tank_Name=row['Tank_Name'],
                    Latitude=row['Latitude'],
                    Longitude=row['Longitude'],
                    Cap_MCM=row['Cap_MCM'],
                    Block=row['Block'],
                    Taluk=row['Taluk'],
                    District=row['District']
                )

            self.stdout.write(self.style.SUCCESS('Water bodies imported successfully!'))
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.WARNING('The Excel file is empty.'))
        except pd.errors.ParserError as e:
            self.stdout.write(self.style.ERROR(f'Error parsing Excel file: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))
