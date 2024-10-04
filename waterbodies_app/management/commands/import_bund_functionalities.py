import pandas as pd
from django.core.management.base import BaseCommand
from waterbodies_app.models import BundFunctionalities  # Adjust the import path as needed

class Command(BaseCommand):
    help = 'Import bund functionalities from an Excel file'

    def handle(self, *args, **options):
        excel_file_path = 'C:\\waterbodies_project\\bundfun.xlsx' # Adjust the path to your Excel file

        # Clear existing records if needed
        BundFunctionalities.objects.all().delete()

        try:
            # Read the Excel file
            bundfun_data = pd.read_excel(excel_file_path)

            # Iterate over the rows in the Excel file and create BundFunctionalities instances
            for _, row in bundfun_data.iterrows():
                BundFunctionalities.objects.create(
                    name=row['name']  # Adjust 'name' if the column name in Excel is different
                )

            self.stdout.write(self.style.SUCCESS('Bund functionalities imported successfully!'))
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.WARNING('The Excel file is empty.'))
        except pd.errors.ParserError as e:
            self.stdout.write(self.style.ERROR(f'Error parsing Excel file: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))
