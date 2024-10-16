# Generated by Django 4.1 on 2024-10-15 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waterbodies_app', '0031_catchmenttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='TankData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tank_num', models.CharField(max_length=100)),
                ('unique_id', models.CharField(max_length=100)),
                ('tank_name', models.CharField(max_length=200)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('village', models.CharField(max_length=200)),
                ('block', models.CharField(max_length=200)),
                ('taluk', models.CharField(max_length=200)),
                ('district', models.CharField(max_length=200)),
                ('subbasin', models.CharField(max_length=200)),
                ('basin', models.CharField(max_length=200)),
                ('section', models.CharField(max_length=200)),
                ('sub_dn', models.CharField(max_length=200)),
                ('division', models.CharField(max_length=200)),
                ('circle', models.CharField(max_length=200)),
                ('region', models.CharField(max_length=200)),
                ('tank_type', models.CharField(max_length=100)),
                ('cap_mcm', models.DecimalField(decimal_places=3, max_digits=10)),
                ('ftl_m', models.DecimalField(decimal_places=3, max_digits=6)),
                ('mwl_m', models.DecimalField(decimal_places=3, max_digits=6)),
                ('tbl_m', models.DecimalField(decimal_places=3, max_digits=6)),
                ('sto_dep_m', models.DecimalField(decimal_places=3, max_digits=6)),
                ('ayacut_ha', models.DecimalField(decimal_places=3, max_digits=10)),
                ('catch_sqkm', models.DecimalField(decimal_places=3, max_digits=10)),
                ('wat_spr_ha', models.DecimalField(decimal_places=3, max_digits=10)),
                ('no_of_weir', models.IntegerField()),
                ('weir_len_m', models.DecimalField(decimal_places=3, max_digits=10)),
                ('no_sluice', models.IntegerField()),
                ('low_sil_m', models.DecimalField(decimal_places=3, max_digits=10)),
                ('bund_len_m', models.DecimalField(decimal_places=3, max_digits=10)),
                ('dis_cusec', models.DecimalField(decimal_places=3, max_digits=10)),
            ],
        ),
    ]
