import pandas as pd
from django.core.management.base import BaseCommand
from waterbodies_app.models import Conditions  # Adjust the import path as needed

class Command(BaseCommand):
    help = 'Import conditions from an Excel file'

    def handle(self, *args, **options):
        excel_file_path = 'C:\\waterbodies_project\\conditions.xlsx'  # Adjust the path to your Excel file

        # Clear existing records if needed
        Conditions.objects.all().delete()

        try:
            # Read the Excel file
            conditions_data = pd.read_excel(excel_file_path)

            # Iterate over the rows in the Excel file and create Conditions instances
            for _, row in conditions_data.iterrows():
                Conditions.objects.create(
                    name=row['name']  # Adjust 'name' if the column name in Excel is different
                )

            self.stdout.write(self.style.SUCCESS('Conditions imported successfully!'))
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.WARNING('The Excel file is empty.'))
        except pd.errors.ParserError as e:
            self.stdout.write(self.style.ERROR(f'Error parsing Excel file: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))
