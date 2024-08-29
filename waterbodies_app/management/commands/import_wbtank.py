import pandas as pd
from django.core.management.base import BaseCommand
from waterbodies_app.models import WaterbodiesTank  # Adjust the import path as needed

class Command(BaseCommand):
    help = 'Import water bodies from an Excel file'

    def handle(self, *args, **options):
        excel_file_path = 'C:\\waterbodies_project\\wbtank.xlsx'  # Replace with the actual path of your Excel file

        # Clear existing records
        WaterbodiesTank.objects.all().delete()

        def convert_to_decimal(value):
            try:
                return float(value)
            except (ValueError, TypeError):
                return None  # or 0.0 or some other default value

        try:
            waterbodies_data = pd.read_excel(excel_file_path)

            for _, row in waterbodies_data.iterrows():
                WaterbodiesTank.objects.create(
                    district=row['District'],
                    latitude=convert_to_decimal(row['Latitude']),
                    longitude=convert_to_decimal(row['Longitude']),
                    block=row.get('Block', ''),
                    panchayat=row.get('Panchayat', ''),
                    village=row.get('Village', ''),
                    tank_name=row.get('Tank_Name', ''),
                    tank_type=row.get('Tank_Type', ''),
                    ayacut_ha=convert_to_decimal(row.get('Ayacut_ha', None)),
                    wat_spr_ar=convert_to_decimal(row.get('Wat_Spr_ar', None)),
                    cap_mcm=convert_to_decimal(row.get('Cap_MCM', None)),
                    no_of_sluices=row.get('No_of_Sluices', None),
                    sluices_type=row.get('Sluices_Type', ''),
                    bund_len_m=convert_to_decimal(row.get('Bund_Len_m', None)),
                    tbl_m=convert_to_decimal(row.get('TBL_m', None)),
                    mwl_m=convert_to_decimal(row.get('MWL_m', None)),
                    ftl_m=convert_to_decimal(row.get('FTL_m', None)),
                    unique_id=row['Unique_id'],
                    sto_depth_m=convert_to_decimal(row.get('Sto_depth_m', None)),
                    catchment=convert_to_decimal(row.get('Catchment', None)),
                    no_of_weirs=row.get('No_of_Weirs', None),
                    weir_length_m=convert_to_decimal(row.get('Weir_length_m', None)),
                    low_sill_m=convert_to_decimal(row.get('Low_sill_m', None)),
                    dis_cusecs=convert_to_decimal(row.get('Dis_cusecs', None)),
                )

            self.stdout.write(self.style.SUCCESS('Water bodies imported successfully!'))
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.WARNING('The Excel file is empty.'))
        except pd.errors.ParserError as e:
            self.stdout.write(self.style.ERROR(f'Error parsing Excel file: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))
