import pandas as pd
from django.core.management.base import BaseCommand
from waterbodies_app.models import BoundaryDropPoints

class Command(BaseCommand):
    help = 'Import boundary data from Excel file'

    def handle(self, *args, **kwargs):
        # Path to your Excel file
        excel_file_path = 'C:\\waterbodies_project\\boundary.xlsx'

        try:
            # Load the Excel file into a pandas DataFrame
            df = pd.read_excel(excel_file_path, engine='openpyxl')

            # Loop through the DataFrame and create objects for each row
            for index, row in df.iterrows():
                BoundaryDropPoints.objects.create(name=row['name'])
            
            self.stdout.write(self.style.SUCCESS('Boundary data imported successfully!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error importing data: {str(e)}"))
