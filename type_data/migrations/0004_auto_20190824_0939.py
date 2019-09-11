# Generated by Django 2.1.7 on 2019-08-24 01:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_platform', '0003_auto_20190824_0939'),
        ('type_data', '0003_auto_20190708_0125'),
    ]

    operations = [
        migrations.CreateModel(
            name='adnormal_failure_report',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('flight_number', models.CharField(max_length=8, verbose_name='航班号')),
                ('occurrence_time', models.DateField(verbose_name='发生时间')),
                ('occurrence_place', models.CharField(max_length=8, verbose_name='发生地点')),
                ('occurrence_phase', models.CharField(max_length=8, verbose_name='发生阶段')),
                ('failure_report_number', models.CharField(max_length=8, verbose_name='故障报告编号')),
                ('failure_description', models.TextField(verbose_name='故障描述')),
                ('delay_hours', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='延误时间/分钟')),
                ('consequence', models.TextField(verbose_name='后果')),
                ('part_replaced_name', models.CharField(max_length=8, verbose_name='拆换件名称')),
                ('part_replaced_number', models.CharField(max_length=8, verbose_name='拆换件件号')),
                ('part_replaced_serial_number', models.CharField(max_length=8, verbose_name='拆换件序号')),
                ('TSR', models.CharField(max_length=8)),
                ('TSN', models.CharField(max_length=8)),
                ('event_survey_summary', models.TextField(verbose_name='事件调查总结')),
                ('belong_to_region', models.CharField(max_length=8, verbose_name='所属区域')),
                ('wether_to_start', models.BooleanField(default=False, verbose_name='是否始发')),
                ('event_analysis', models.TextField(verbose_name='事件分析')),
                ('delay_quality', models.CharField(max_length=8, verbose_name='延误定性')),
                ('improvement_measures_resolutions', models.TextField(verbose_name='改进措施与决议')),
                ('departure_planned_time', models.DateField(verbose_name='计划起飞时间')),
                ('departure_actual_time', models.DateField(verbose_name='实际起飞时间')),
                ('major', models.CharField(max_length=8, verbose_name='专业')),
            ],
            options={
                'verbose_name': '航班不正常报告',
                'verbose_name_plural': '航班不正常报告',
                'ordering': ('delay_quality',),
            },
        ),
        migrations.CreateModel(
            name='aircraft',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('aircraft_registration_number', models.CharField(max_length=100, verbose_name='航空器注册号')),
                ('aircraft_serial_number', models.CharField(max_length=100, verbose_name='系列号')),
                ('production_serial_number', models.CharField(max_length=100, verbose_name='产品系列号')),
                ('acmodel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aircraft_acmodel', to='data_platform.acmodel')),
            ],
            options={
                'verbose_name': '航空器',
                'verbose_name_plural': '航空器',
                'ordering': ('aircraft_registration_number',),
            },
        ),
        migrations.CreateModel(
            name='aircraft_info',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('monthly_available_days', models.DecimalField(decimal_places=0, max_digits=3, verbose_name='在用架日')),
                ('monthly_total_flight_hours', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='当月总飞行时间')),
                ('monthly_flight_times', models.DecimalField(decimal_places=0, max_digits=6, verbose_name='当月总起落架次')),
                ('monthly_service_flight_hours', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='当月营运飞行时间')),
                ('monthly_service_flight_times', models.DecimalField(decimal_places=0, max_digits=6, verbose_name='当月营运起落次数')),
                ('cumulative_flight_hours', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='累积飞行时间')),
                ('cumulative_flight_times', models.DecimalField(decimal_places=0, max_digits=9, verbose_name='累积飞行起落次数')),
                ('date', models.DateField(verbose_name='日期')),
                ('company', models.CharField(max_length=100, verbose_name='公司')),
                ('acmodel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aircraft_information_acmodel', to='data_platform.acmodel')),
            ],
            options={
                'verbose_name': '航空器信息',
                'verbose_name_plural': '航空器信息',
                'ordering': ('acmodel',),
            },
        ),
        migrations.CreateModel(
            name='aircraft_info_change',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('in_or_out', models.CharField(max_length=100, verbose_name='引进或转出')),
                ('current_aircraft_operator', models.CharField(max_length=100, verbose_name='当前所属航空器运营人')),
                ('original_aircraft_operator', models.CharField(max_length=100, verbose_name='原所属航空器运营人')),
                ('in_or_out_reason', models.CharField(max_length=100, verbose_name='引入或转出原因')),
                ('date', models.DateField(verbose_name='日期')),
                ('method', models.CharField(max_length=100, verbose_name='方式')),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aircraft_info_change_aircraft', to='type_data.aircraft')),
            ],
            options={
                'verbose_name': '航空器信息变化表',
                'verbose_name_plural': '航空器信息变化表',
                'ordering': ('date',),
            },
        ),
        migrations.CreateModel(
            name='apu_using_record',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('apu_part_number', models.CharField(max_length=20, verbose_name='APU件号')),
                ('monthly_service_hours', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='当月使用时间')),
                ('monthly_service_cycles', models.DecimalField(decimal_places=0, max_digits=6, verbose_name='当月使用循环')),
                ('total_service_hours', models.DecimalField(decimal_places=0, max_digits=9, verbose_name='总使用时间')),
                ('total_service_cycles', models.DecimalField(decimal_places=0, max_digits=9, verbose_name='总使用循环')),
                ('scheduled_replacement', models.CharField(max_length=100, verbose_name='计划拆换')),
                ('unscheduled_replacement', models.CharField(max_length=100, verbose_name='非计划拆换')),
                ('date', models.DateField(verbose_name='日期')),
                ('acmodel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apu_using_record_acmodel', to='data_platform.acmodel')),
            ],
            options={
                'verbose_name': 'APU使用记录',
                'verbose_name_plural': 'APU使用记录',
                'ordering': ('apu_part_number',),
            },
        ),
        migrations.CreateModel(
            name='engine',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('engine_serial_number', models.CharField(max_length=100, verbose_name='发动机序号')),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='engine_aircraft', to='type_data.aircraft')),
            ],
            options={
                'verbose_name': '发动机',
                'verbose_name_plural': '发动机',
                'ordering': ('engine_type',),
            },
        ),
        migrations.CreateModel(
            name='engine_air_stop_record',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('flight_number', models.CharField(max_length=8, verbose_name='航班号')),
                ('installed_position', models.CharField(max_length=4, verbose_name='装机位置')),
                ('air_stop_time', models.DateField(verbose_name='空中停车时间')),
                ('occurrence_phase', models.CharField(max_length=8, verbose_name='发生阶段')),
                ('occurrence_place', models.CharField(max_length=8, verbose_name='发生地点')),
                ('event_description', models.TextField(verbose_name='事件描述')),
                ('reason_analysis', models.TextField(verbose_name='原因分析')),
                ('engine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='engine_air_stop_record_engine', to='type_data.engine')),
            ],
            options={
                'verbose_name': '发动机停车记录',
                'verbose_name_plural': '发动机停车记录',
                'ordering': ('engine',),
            },
        ),
        migrations.CreateModel(
            name='engine_info_change',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('in_or_out', models.CharField(max_length=100, verbose_name='引进或转出')),
                ('current_aircraft_operator', models.CharField(max_length=100, verbose_name='当前所属航空器运营人')),
                ('original_aircraft_operator', models.CharField(max_length=100, verbose_name='原所属航空器运营人')),
                ('in_or_out_reason', models.CharField(max_length=100, verbose_name='引入或转出原因')),
                ('date', models.DateField(verbose_name='日期')),
                ('engine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='engine_info_change_engine', to='type_data.engine')),
            ],
            options={
                'verbose_name': '发动机信息变化表',
                'verbose_name_plural': '发动机信息变化表',
                'ordering': ('date',),
            },
        ),
        migrations.CreateModel(
            name='engine_replacement_type',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('engine_replacement_type', models.CharField(max_length=50, verbose_name='拆下发动机序列号')),
            ],
            options={
                'verbose_name': '发动机拆换型号',
                'verbose_name_plural': '发动机拆换型号',
                'ordering': ('engine_replacement_type',),
            },
        ),
        migrations.CreateModel(
            name='engine_type',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('engine_type_number', models.CharField(max_length=100, verbose_name='发动机型号')),
            ],
            options={
                'verbose_name': '发动机型号',
                'verbose_name_plural': '发动机型号',
                'ordering': ('engine_type_number',),
            },
        ),
        migrations.CreateModel(
            name='engine_using_record',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('installed_position', models.CharField(max_length=4, verbose_name='装机位置')),
                ('monthly_service_hours', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='当月使用时间')),
                ('monthly_service_cycles', models.DecimalField(decimal_places=0, max_digits=6, verbose_name='当月使用循环')),
                ('if_overhaul', models.BooleanField(default=False, verbose_name='当月是否大修')),
                ('service_hours_after_repair', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='修后使用时间')),
                ('service_cycles_after_repair', models.DecimalField(decimal_places=0, max_digits=6, verbose_name='修后使用循环')),
                ('total_service_hours', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='总使用时间')),
                ('total_service_cycles', models.DecimalField(decimal_places=0, max_digits=9, verbose_name='总使用循环')),
                ('date', models.DateField(verbose_name='日期')),
                ('replacement_reason', models.TextField(verbose_name='拆换原因')),
                ('maintenance', models.TextField(verbose_name='维修')),
                ('scope_of_work', models.TextField(verbose_name='工作范围')),
                ('engine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='engine', to='type_data.engine')),
            ],
            options={
                'verbose_name': '发动机使用记录',
                'verbose_name_plural': '发动机使用记录',
                'ordering': ('engine',),
            },
        ),
        migrations.CreateModel(
            name='failure_mode_bank',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('failure_mode', models.TextField(verbose_name='故障模式')),
                ('failure_consequence', models.TextField(verbose_name='故障影响后果')),
                ('failure_reason', models.TextField(verbose_name='故障原因')),
                ('failure_troubleshooting', models.TextField(verbose_name='故障解决措施')),
                ('acmodel', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='failure_mode_bank_acmodel', to='data_platform.acmodel')),
            ],
            options={
                'verbose_name': '故障模式库',
                'verbose_name_plural': '故障模式库',
                'ordering': ('failure_mode',),
            },
        ),
        migrations.CreateModel(
            name='failure_report_record',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('flight_number', models.CharField(max_length=8, verbose_name='航班号')),
                ('occurrence_time', models.DateField(verbose_name='发生时间')),
                ('occurrence_place', models.CharField(max_length=8, verbose_name='发生地点')),
                ('failure_report_number', models.CharField(max_length=8, verbose_name='故障报告编号')),
                ('occurrence_phase', models.CharField(max_length=8, verbose_name='发生阶段')),
                ('report_source', models.TextField(verbose_name='报告来源')),
                ('failure_name_code', models.CharField(max_length=8, verbose_name='故障名称/编码')),
                ('failure_description', models.TextField(verbose_name='故障描述')),
                ('failure_phenomenon', models.TextField(verbose_name='故障现象')),
                ('troubleshooting_measures', models.TextField(verbose_name='处理措施')),
                ('maintenance_level', models.CharField(max_length=8, verbose_name='维修级别')),
                ('failure_class', models.CharField(max_length=8, verbose_name='故障类别')),
                ('importance_degree', models.CharField(max_length=8, verbose_name='重要程度')),
                ('information_category_content', models.TextField(verbose_name='信息类别内容')),
                ('failure_type', models.CharField(max_length=8, verbose_name='故障类别')),
                ('airport_terminal', models.CharField(max_length=8, verbose_name='航站')),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='failure_report_record_aircraft', to='type_data.aircraft')),
            ],
            options={
                'verbose_name': '故障报告记录',
                'verbose_name_plural': '故障报告记录',
                'ordering': ('importance_degree',),
            },
        ),
        migrations.CreateModel(
            name='record_of_engine_replaced',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('installed_position', models.CharField(max_length=100, verbose_name='装机位置')),
                ('remove_time', models.DateField(verbose_name='拆下时间')),
                ('replacement_type', models.CharField(max_length=100, verbose_name='拆卸类型')),
                ('check_and_discovery', models.CharField(max_length=100, verbose_name='检查发现')),
                ('maintenance_measure', models.CharField(max_length=100, verbose_name='维修措施')),
                ('single_service_hours', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='本次使用时间')),
                ('single_service_cycles', models.DecimalField(decimal_places=0, max_digits=6, verbose_name='本次使用循环')),
                ('total_service_hours', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='总使用时间')),
                ('total_service_cycles', models.DecimalField(decimal_places=0, max_digits=9, verbose_name='总使用循环')),
                ('replacement_reason', models.CharField(max_length=100, verbose_name='拆换原因')),
                ('scope_of_work', models.CharField(max_length=100, verbose_name='工作范围')),
                ('engine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='record_of_engine_replace_engine', to='type_data.engine')),
            ],
            options={
                'verbose_name': '发动机拆换记录',
                'verbose_name_plural': '发动机拆换记录',
                'ordering': ('engine',),
            },
        ),
        migrations.CreateModel(
            name='record_of_part_replaced',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('flight_number', models.CharField(max_length=100, verbose_name='航班号')),
                ('date', models.DateField(verbose_name='时间')),
                ('replacement_reason', models.CharField(max_length=100, verbose_name='拆换原因')),
                ('failure_discovery', models.CharField(max_length=100, verbose_name='故障发现')),
                ('failure_confirmation', models.CharField(max_length=100, verbose_name='故障确认')),
                ('part_replaced_name', models.CharField(max_length=100, verbose_name='拆换件名称')),
                ('part_replaced_numbers', models.CharField(max_length=100, verbose_name='拆下件数量')),
                ('part_installed_numbers', models.CharField(max_length=100, verbose_name='安装件数量')),
                ('part_removed_serial_number', models.CharField(max_length=100, verbose_name='拆下件序列号')),
                ('part_installed_serial_number', models.CharField(max_length=100, verbose_name='安装件序列号')),
                ('replacement_type', models.CharField(max_length=100, verbose_name='拆换工作类型')),
                ('maintenance_level', models.CharField(max_length=100, verbose_name='维修级别')),
                ('advanced_device', models.CharField(max_length=100, verbose_name='高级设备')),
                ('failure_handling', models.CharField(max_length=100, verbose_name='故障处理')),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='record_of_part_replace_aircraft', to='type_data.aircraft')),
            ],
            options={
                'verbose_name': '部件拆换记录',
                'verbose_name_plural': '部件拆换记录',
                'ordering': ('part_replaced_name',),
            },
        ),
        migrations.CreateModel(
            name='record_of_scheduled_maintenance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('task_number', models.CharField(max_length=100, verbose_name='工卡号/任务号')),
                ('date', models.DateField(verbose_name='日期')),
                ('task_description', models.CharField(max_length=100, verbose_name='任务描述')),
                ('task_source', models.CharField(max_length=100, verbose_name='任务来源')),
                ('check_intervals', models.CharField(max_length=100, verbose_name='检查间隔')),
                ('reference_material', models.CharField(max_length=100, verbose_name='参考资料')),
                ('cumulative_flight_hours', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='累计飞行时间')),
                ('cumulative_flight_times', models.DecimalField(decimal_places=0, max_digits=9, verbose_name='累计起落次数')),
                ('flight_hours_after_last_check', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='上次检查后飞行时间')),
                ('flight_times_after_last_check', models.DecimalField(decimal_places=0, max_digits=9, verbose_name='上次检查后起落次数')),
                ('check_discovery', models.CharField(max_length=100, verbose_name='检查发现')),
                ('troubleshooting_measures', models.CharField(max_length=100, verbose_name='排故措施')),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='record_of_scheduled_maintenance_aircraft', to='type_data.aircraft')),
            ],
            options={
                'verbose_name': '计划维修记录',
                'verbose_name_plural': '计划维修记录',
                'ordering': ('task_number',),
            },
        ),
        migrations.CreateModel(
            name='use_difficult_report',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('flight_number', models.CharField(max_length=8, verbose_name='航班号')),
                ('report_number', models.CharField(max_length=8, verbose_name='报告编号')),
                ('service_varity', models.CharField(max_length=8, verbose_name='运营种类')),
                ('occurrence_time', models.DateField(verbose_name='发生时间')),
                ('occurrence_place', models.CharField(max_length=8, verbose_name='发生地点')),
                ('occurrence_phase', models.CharField(max_length=8, verbose_name='发生阶段')),
                ('event_description_improvement_measures', models.TextField(verbose_name='问题描述和纠正措施')),
                ('preventive_emergency_measures', models.TextField(verbose_name='预防紧急措施')),
                ('failure_exchange_part_name', models.CharField(max_length=8, verbose_name='故障件/更换件名称')),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='use_difficult_report_aircraft', to='type_data.aircraft')),
            ],
            options={
                'verbose_name': '使用困难报告',
                'verbose_name_plural': '使用困难报告',
                'ordering': ('service_varity',),
            },
        ),
        migrations.RemoveField(
            model_name='ac',
            name='acmodel',
        ),
        migrations.DeleteModel(
            name='aputime',
        ),
        migrations.RemoveField(
            model_name='engine_info',
            name='ac',
        ),
        migrations.RemoveField(
            model_name='entime',
            name='en_sn',
        ),
        migrations.RemoveField(
            model_name='flytime',
            name='ac',
        ),
        migrations.RemoveField(
            model_name='fm',
            name='acmodel',
        ),
        migrations.RemoveField(
            model_name='fm',
            name='ata',
        ),
        migrations.AlterModelOptions(
            name='ata',
            options={'ordering': ('chapter',), 'verbose_name': 'ATA章节', 'verbose_name_plural': 'ATA章节'},
        ),
        migrations.DeleteModel(
            name='ac',
        ),
        migrations.DeleteModel(
            name='engine_info',
        ),
        migrations.DeleteModel(
            name='entime',
        ),
        migrations.DeleteModel(
            name='flytime',
        ),
        migrations.DeleteModel(
            name='fm',
        ),
        migrations.AddField(
            model_name='use_difficult_report',
            name='ata',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='use_difficult_report_ata', to='type_data.ata'),
        ),
        migrations.AddField(
            model_name='record_of_scheduled_maintenance',
            name='ata',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='record_of_scheduled_maintenance_ata', to='type_data.ata'),
        ),
        migrations.AddField(
            model_name='record_of_part_replaced',
            name='ata',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='record_of_part_replace_ata', to='type_data.ata'),
        ),
        migrations.AddField(
            model_name='failure_report_record',
            name='ata',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='failure_report_record_ata', to='type_data.ata'),
        ),
        migrations.AddField(
            model_name='failure_mode_bank',
            name='ata',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='failure_mode_bank_ata', to='type_data.ata'),
        ),
        migrations.AddField(
            model_name='engine',
            name='engine_replacement_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='engine_engine_replacement_type', to='type_data.engine_replacement_type'),
        ),
        migrations.AddField(
            model_name='engine',
            name='engine_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='engine_engine_type', to='type_data.engine_type'),
        ),
        migrations.AddField(
            model_name='adnormal_failure_report',
            name='aircraft',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adnormal_failure_report_aircraft', to='type_data.aircraft'),
        ),
        migrations.AddField(
            model_name='adnormal_failure_report',
            name='ata',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adnormal_failure_report_ata', to='type_data.ata'),
        ),
    ]