# waterbodies/management/commands/import_ponds.py
import pandas as pd
from django.core.management.base import BaseCommand
from waterbodies_app.models import Pond  # Import your Pond model here

class Command(BaseCommand):
    help = 'Import ponds from Excel file'

    def handle(self, *args, **options):
        excel_file_path = 'C:\\waterbodies_project\\pond.xlsx'  # Replace with the actual path of your Excel file

        # Clear existing records
        Pond.objects.all().delete()

        try:
            ponds_data = pd.read_excel(excel_file_path)

            for _, row in ponds_data.iterrows():
                name = row['Waterbody Name'] if not pd.isna(row['Waterbody Name']) else ''
                district = row['District'] if not pd.isna(row['District']) else ''
                taluk = row['Taluk'] if not pd.isna(row['Taluk']) else ''
                block = row['Block'] if not pd.isna(row['Block']) else ''
                village = row['Village'] if not pd.isna(row['Village']) else ''
                waterbody_type = row['Water Body Type'] if not pd.isna(row['Water Body Type']) else ''
                waterbody_id = row['Waterbody Id'] if not pd.isna(row['Waterbody Id']) else ''
                survey_number = row['Survey Number'] if not pd.isna(row['Survey Number']) else ''
                ownership = row['Ownership'] if not pd.isna(row['Ownership']) else ''
                availability = row['Waterbody Availability'] if not pd.isna(row['Waterbody Availability']) else ''

                Pond.objects.create(
                    name=name,
                    district=district,
                    taluk=taluk,
                    block=block,
                    village=village,
                    waterbody_type=waterbody_type,
                    waterbody_id=waterbody_id,
                    survey_number=survey_number,
                    ownership=ownership,
                    availability=availability
                )

            self.stdout.write(self.style.SUCCESS('Ponds imported successfully!'))
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.WARNING('The Excel file is empty.'))
        except pd.errors.ParserError as e:
            self.stdout.write(self.style.ERROR(f'Error parsing Excel file: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))
