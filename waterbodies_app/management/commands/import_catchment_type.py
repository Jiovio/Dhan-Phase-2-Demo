import pandas as pd
from django.core.management.base import BaseCommand
from waterbodies_app.models import CatchmentType  # Adjust the import path as needed

class Command(BaseCommand):
    help = 'Import catchment types from an Excel file'

    def handle(self, *args, **options):
        excel_file_path = 'C:\\waterbodies_project\\catchment.xlsx' # Adjust the path to your Excel file

        # Clear existing records if needed
        CatchmentType.objects.all().delete()

        try:
            # Read the Excel file
            catchment_data = pd.read_excel(excel_file_path)

            # Iterate over the rows in the Excel file and create CatchmentType instances
            for _, row in catchment_data.iterrows():
                CatchmentType.objects.create(
                    name=row['name']  # Adjust 'name' if the column name in Excel is different
                )

            self.stdout.write(self.style.SUCCESS('Catchment types imported successfully!'))
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.WARNING('The Excel file is empty.'))
        except pd.errors.ParserError as e:
            self.stdout.write(self.style.ERROR(f'Error parsing Excel file: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))
