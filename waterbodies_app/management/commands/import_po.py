import pandas as pd
from django.core.management.base import BaseCommand
from waterbodies_app.models import PoOwaterbody  # Update this with your actual model path

class Command(BaseCommand):
    help = 'Import water bodies from an Excel file'

    def handle(self, *args, **options):
        excel_file_path = 'C:\\waterdams_project\\DRDApo.xlsx'  # Update with the path to your Excel file

        def convert_to_decimal(value):
            try:
                return float(value)
            except (ValueError, TypeError):
                return None

        try:
            # Load data from the Excel file
            waterbodies_data = pd.read_excel(excel_file_path)

            # Clear all existing records
            PoOwaterbody.objects.all().delete()

            # Import the new data
            for _, row in waterbodies_data.iterrows():
                PoOwaterbody.objects.create(
                    unique_id=row['Unique_id'],
                    ponds_oo=row.get('Ponds___Oo', ''),
                    latitude=convert_to_decimal(row['Latitude']),
                    longitude=convert_to_decimal(row['Longitude']),
                    taluk=row.get('Taluk', ''),
                    block=row.get('Block', ''),
                    panchayat=row.get('Panchayat', ''),
                    village=row.get('Village', ''),
                    pond_type=row.get('Pond_Type', ''),
                    cap_mcm=convert_to_decimal(row.get('Cap_MCM', None)),
                    fpl_m=convert_to_decimal(row.get('FPL__m', None)),
                    mwl_m=convert_to_decimal(row.get('MWL_m', None)),
                    pbl_m=convert_to_decimal(row.get('PBL__m', None)),
                    sto_dep_m=convert_to_decimal(row.get('Sto_dep_m', None)),
                    catchment=convert_to_decimal(row.get('Catchment', None)),
                    wat_spr_ar=convert_to_decimal(row.get('Wat_spr_ar', None)),
                    bund_len_m=convert_to_decimal(row.get('Bund_Len_m', None)),
                    dis_cusecs=convert_to_decimal(row.get('Dis_cusecs', None)),
                )

            self.stdout.write(self.style.SUCCESS('Water bodies imported successfully!'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {excel_file_path}'))
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.WARNING('The Excel file is empty.'))
        except pd.errors.ParserError as e:
            self.stdout.write(self.style.ERROR(f'Error parsing Excel file: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))
