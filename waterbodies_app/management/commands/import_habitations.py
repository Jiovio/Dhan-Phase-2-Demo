# import_habitations.py

import pandas as pd
from django.core.management.base import BaseCommand
from waterbodies_app.models import Habitation  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = 'Import habitations from an Excel file'

    def handle(self, *args, **options):
        excel_file_path = 'C:\\waterbodies_project\\waterBodyAdmin_habitation.xlsx'  # Replace with the actual path of your Excel file

        # Clear existing records
        Habitation.objects.all().delete()

        try:
            # Read the Excel file
            habitations_data = pd.read_excel(excel_file_path)

            # Iterate over the rows in the Excel file and create Habitation instances
            for _, row in habitations_data.iterrows():
                Habitation.objects.create(
                    district_code=row['DistrictCode'],  # Adjust these column names to match your Excel file
                    district=row['District'],
                    block_code=row['BlockCode'],
                    block=row['Block'],
                    village_code=row['VillageCode'],
                    village=row['Village'],
                    habitation_code=row['HabitationCode'],
                    habitation=row['Habitation']
                )

            self.stdout.write(self.style.SUCCESS('Habitations imported successfully!'))
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.WARNING('The Excel file is empty.'))
        except pd.errors.ParserError as e:
            self.stdout.write(self.style.ERROR(f'Error parsing Excel file: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))
