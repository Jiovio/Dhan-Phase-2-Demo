import pandas as pd
from django.core.management.base import BaseCommand
from waterbodies_app.models import Tank  # Replace 'myapp' with your actual app name

class Command(BaseCommand):
    help = 'Import tanks from Excel file'

    def handle(self, *args, **options):
        excel_file_path = 'C:\\waterbodies_project\\tank.xlsx'  # Replace with the actual path of your Excel file

        try:
            tanks_data = pd.read_excel(excel_file_path)

            for _, row in tanks_data.iterrows():
                Tank.objects.create(
                    tank_name=row.get('Tank Name', '') if pd.notna(row.get('Tank Name', '')) else '',
                    district=row.get('District', '') if pd.notna(row.get('District', '')) else '',
                    taluk=row.get('Taluk', '') if pd.notna(row.get('Taluk', '')) else '',
                    block=row.get('Block', '') if pd.notna(row.get('Block', '')) else '',
                    village=row.get('Village', '') if pd.notna(row.get('Village', '')) else '',
                    jurisdiction_name=row.get('Jurisdiction Name', '') if pd.notna(row.get('Jurisdiction Name', '')) else '',
                    ward=row.get('Ward', '') if pd.notna(row.get('Ward', '')) else '',
                    waterbody_type=row.get('Water Body Type', '') if pd.notna(row.get('Water Body Type', '')) else '',
                    waterbody_id=row.get('Waterbody Id', '') if pd.notna(row.get('Waterbody Id', '')) else '',
                    survey_number=row.get('Survey Number', '') if pd.notna(row.get('Survey Number', '')) else '',
                    ownership=row.get('Ownership', '') if pd.notna(row.get('Ownership', '')) else '',
                    waterbody_availability=row.get('Waterbody Availability', '') if pd.notna(row.get('Waterbody Availability', '')) else ''
                )

            self.stdout.write(self.style.SUCCESS('Tanks imported successfully!'))
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.WARNING('The Excel file is empty.'))
        except pd.errors.ParserError as e:
            self.stdout.write(self.style.ERROR(f'Error parsing Excel file: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))
