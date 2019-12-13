# Generated by Django 2.2.1 on 2019-12-11 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='aircraft_info',
            fields=[
                ('aircraft_serial_number', models.TextField(primary_key=True, serialize=False, verbose_name='航空器注册号')),
                ('aircraft_owner', models.TextField(verbose_name='飞机拥有者')),
                ('cumulative_flight_cycles', models.DecimalField(decimal_places=0, max_digits=7, verbose_name='飞行循环')),
                ('cumulative_flight_hours', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='飞行小时')),
                ('flight_character', models.TextField(verbose_name='飞行性质')),
            ],
            options={
                'verbose_name': '航空器信息',
                'verbose_name_plural': '航空器信息',
                'ordering': ('aircraft_serial_number',),
            },
        ),
        migrations.CreateModel(
            name='aircraft_type',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('aircraft_type_number', models.TextField(verbose_name='机型编号')),
            ],
            options={
                'verbose_name': '机型',
                'verbose_name_plural': '机型',
                'ordering': ('aircraft_type_number',),
            },
        ),
        migrations.CreateModel(
            name='ATA',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('major', models.TextField(verbose_name='专业')),
                ('chapter', models.DecimalField(decimal_places=0, max_digits=3, verbose_name='章')),
                ('section', models.DecimalField(decimal_places=0, max_digits=3, verbose_name='节')),
                ('subject', models.DecimalField(decimal_places=0, max_digits=3, verbose_name='题')),
            ],
            options={
                'verbose_name': 'ATA章节',
                'verbose_name_plural': 'ATA章节',
                'ordering': ('chapter', 'section', 'subject'),
            },
        ),
        migrations.CreateModel(
            name='original_event_number',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('original_event_url', models.CharField(max_length=1000, verbose_name='链接')),
            ],
            options={
                'verbose_name': '原始事件编号',
                'verbose_name_plural': '原始事件编号',
            },
        ),
        migrations.CreateModel(
            name='problem_info',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('problem_number', models.CharField(max_length=1000, verbose_name='问题编号')),
                ('failure_part_number', models.CharField(max_length=1000, verbose_name='故障件编号')),
                ('failure_part_name', models.CharField(max_length=1000, verbose_name='故障件名称')),
                ('handling_action', models.TextField(verbose_name='处理意见')),
                ('if_affect_reliability', models.BooleanField(default=False, verbose_name='是否影响可靠性')),
                ('if_affect_safety', models.BooleanField(default=False, verbose_name='是否安全性')),
                ('if_failure', models.BooleanField(default=False, verbose_name='是否是故障')),
                ('occurrence_time', models.IntegerField(verbose_name='发生次数')),
                ('problem_description', models.TextField(verbose_name='问题描述')),
                ('troubleshooting', models.TextField(verbose_name='排故概况')),
                ('problem_state', models.CharField(max_length=1000, verbose_name='问题关闭情况')),
            ],
            options={
                'verbose_name': '问题清单',
                'verbose_name_plural': '问题清单',
                'ordering': ('occurrence_time',),
            },
        ),
        migrations.CreateModel(
            name='event_info',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('internal_number', models.CharField(max_length=1000, verbose_name='内部编号')),
                ('attachment_info', models.TextField(verbose_name='附件信息')),
                ('corrective_action', models.TextField(verbose_name='纠正文本')),
                ('event_description', models.TextField(verbose_name='问题描述')),
                ('failure_number', models.CharField(max_length=1000, verbose_name='故障编号')),
                ('failure_part_name', models.CharField(max_length=1000, verbose_name='故障件名称')),
                ('failure_part_number', models.CharField(max_length=1000, verbose_name='故障件件号')),
                ('flight_phase', models.CharField(max_length=1000, verbose_name='飞行阶段')),
                ('handling_suggestion', models.TextField(verbose_name='处理意见')),
                ('if_tech_question', models.BooleanField(default=False, verbose_name='是否技术问题')),
                ('occurrence_time', models.DateTimeField(verbose_name='发生时间')),
                ('other_number', models.CharField(max_length=1000, verbose_name='其他编号')),
                ('task_classification', models.CharField(max_length=1000, verbose_name='任务分类')),
                ('task_number', models.CharField(max_length=1000, verbose_name='任务编号')),
                ('troubleshooting', models.TextField(verbose_name='排故概况')),
                ('failure_handling', models.TextField(verbose_name='故障处理')),
                ('event_state', models.CharField(max_length=1000, verbose_name='问题关闭情况')),
                ('detail_information_source', models.CharField(max_length=1000, null=True, verbose_name='详细信息来源')),
                ('remarks', models.TextField(verbose_name='备注')),
                ('ATA', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_info_ATA', to='intra_type_data.ATA')),
                ('aircraft_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_info_aircraft_info', to='intra_type_data.aircraft_info')),
                ('original_event_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='original_event_number', to='intra_type_data.original_event_number')),
                ('problem_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_info_problem_info', to='intra_type_data.problem_info')),
            ],
            options={
                'verbose_name': '事件清单',
                'verbose_name_plural': '事件清单',
                'ordering': ('occurrence_time',),
            },
        ),
        migrations.AddField(
            model_name='aircraft_info',
            name='aircraft_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aircraft_info_aircraft_type', to='intra_type_data.aircraft_type'),
        ),
    ]
