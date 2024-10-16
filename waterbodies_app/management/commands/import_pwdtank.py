import pandas as pd
from django.core.management.base import BaseCommand
from waterbodies_app.models import TankData  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = 'Import tank data from an Excel file into the TankData model'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']  # Correct way to access the file path argument

        # Read the Excel file using pandas
        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading the Excel file: {e}"))
            return

        # Iterate over the rows in the dataframe and save the data to the model
        for index, row in df.iterrows():
            tank_data = TankData(
                tank_num=row['TANK_NUM'],
                unique_id=row['Unique_id'],
                tank_name=row['Tank_Name'],
                latitude=row['Latitude'],
                longitude=row['Longitude'],
                village=row['Village'],
                block=row['Block'],
                taluk=row['Taluk'],
                district=row['District'],
                subbasin=row['Subbasin'],
                basin=row['Basin'],
                section=row['Section'],
                sub_dn=row['Sub_Dn'],
                division=row['Division'],
                circle=row['Circle'],
                region=row['Region'],
                tank_type=row['Tank_Type'],
                cap_mcm=row['Cap_MCM'],
                ftl_m=row['FTL_m'],
                mwl_m=row['MWL_m'],
                tbl_m=row['TBL_m'],
                sto_dep_m=row['Sto_Dep_m'],
                ayacut_ha=row['Ayacut_ha'],
                catch_sqkm=row['Catch_sqkm'],
                wat_spr_ha=row['Wat_Spr_ha'],
                no_of_weir=row['No_of_Weir'],
                weir_len_m=row['Weir_Len_m'],
                no_sluice=row['No_Sluice'],
                low_sil_m=row['Low_Sil_m'],
                bund_len_m=row['Bund_Len_m'],
                dis_cusec=row['Dis_cusec'],
            )
            tank_data.save()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
