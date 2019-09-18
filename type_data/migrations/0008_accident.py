# Generated by Django 2.2.2 on 2019-09-18 02:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('type_data', '0007_airline_maintenance_hours_statistics_flight_data_flight_hours_and_upanddown_amounts_table_mtbur_unsc'),
    ]

    operations = [
        migrations.CreateModel(
            name='accident',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField(verbose_name='事故名称')),
                ('flight_number', models.TextField(verbose_name='航班号')),
                ('manufacture_country', models.TextField(verbose_name='运营商所属国家')),
                ('operator', models.TextField(verbose_name='运营商')),
                ('occurrence_time', models.DateField(max_length=8, verbose_name='事故时间')),
                ('flight_type', models.TextField(verbose_name='飞行性质')),
                ('flight_phase', models.TextField(verbose_name='阶段')),
                ('death_toll', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='死亡人数')),
                ('occurrence_region', models.TextField(verbose_name='事故地区')),
                ('occurrence_place', models.TextField(verbose_name='事故地点')),
                ('departure', models.TextField(verbose_name='出发地')),
                ('destination', models.TextField(verbose_name='目的地')),
                ('accident_factor', models.TextField(verbose_name='事故因素分类')),
                ('accident_level', models.TextField(verbose_name='事故等级')),
                ('description', models.TextField(verbose_name='事故描述')),
                ('reason', models.TextField(verbose_name='原因分析')),
                ('measurement', models.TextField(verbose_name='采取的措施')),
                ('design_suggestion', models.TextField(verbose_name='设计建议')),
                ('safety_suggestion', models.TextField(verbose_name='安全性建议')),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accident_aircraft', to='type_data.aircraft')),
            ],
            options={
                'verbose_name': '事故事件',
                'verbose_name_plural': '事故事件',
                'ordering': ('title', 'death_toll'),
            },
        ),
    ]