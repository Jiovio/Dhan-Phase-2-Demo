import pandas as pd
from django.core.management.base import BaseCommand
from waterbodies_app.models import AyacutNonCultivation  # Adjust based on your app name

class Command(BaseCommand):
    help = 'Import ayacut data from an Excel file'

    def handle(self, *args, **options):
        excel_file_path = 'C:\\waterbodies_project\\ayacut.xlsx'  # Replace with the actual path of your Excel file

        try:
            # Read the Excel file
            ayacut_data = pd.read_excel(excel_file_path)

            # Clear existing records (optional)
            AyacutNonCultivation.objects.all().delete()

            # Iterate over the rows in the Excel file and create AyacutNonCultivation instances
            for _, row in ayacut_data.iterrows():
                AyacutNonCultivation.objects.create(
                    name=row['name'],  # Adjust 'name' if it’s different in your Excel
                )

            self.stdout.write(self.style.SUCCESS('Ayacut data imported successfully!'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {excel_file_path}'))
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.WARNING('The Excel file is empty.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))
