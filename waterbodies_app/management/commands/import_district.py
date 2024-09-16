import pandas as pd
from django.core.management.base import BaseCommand
from waterbodies_app.models import District  # Adjust the import path as needed

class Command(BaseCommand):
    help = 'Import districts from an Excel file'

    def handle(self, *args, **options):
        excel_file_path = 'C:\\waterbodies_project\\waterBodyadmin_district.xlsx'  # Replace with the actual path of your Excel file

        # Clear existing records
        District.objects.all().delete()

        try:
            # Read the Excel file
            districts_data = pd.read_excel(excel_file_path)

            # Iterate over the rows in the Excel file and create District instances
            for _, row in districts_data.iterrows():
                District.objects.create(
                    code=row['code'],  # Adjust these column names to match your Excel file
                    name=row['name']
                )

            self.stdout.write(self.style.SUCCESS('Districts imported successfully!'))
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.WARNING('The Excel file is empty.'))
        except pd.errors.ParserError as e:
            self.stdout.write(self.style.ERROR(f'Error parsing Excel file: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))
