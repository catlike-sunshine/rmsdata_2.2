# Generated by Django 2.1.7 on 2019-08-24 01:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_platform', '0002_auto_20190708_0102'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='acmodel',
            options={'ordering': ('aircraft_type',), 'verbose_name': '飞机型号', 'verbose_name_plural': '飞机型号'},
        ),
        migrations.RenameField(
            model_name='acmodel',
            old_name='expanded_acmodel',
            new_name='aircraft_serial_number',
        ),
        migrations.RenameField(
            model_name='acmodel',
            old_name='basic_acmodel',
            new_name='aircraft_type',
        ),
    ]
