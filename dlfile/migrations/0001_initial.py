# Generated by Django 2.1.7 on 2019-07-09 11:47

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='file',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=200)),
                ('content', ckeditor.fields.RichTextField(verbose_name='数据说明')),
                ('date', models.DateField(verbose_name='数据产生时间')),
                ('file', models.FileField(blank=True, upload_to='datafile/%Y/%m/%d')),
            ],
            options={
                'verbose_name': '数据列表',
                'verbose_name_plural': '数据列表',
            },
        ),
        migrations.CreateModel(
            name='file_category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='名称')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='简称')),
                ('content', ckeditor.fields.RichTextField(verbose_name='说明')),
            ],
            options={
                'verbose_name': '数据分类',
                'verbose_name_plural': '数据分类',
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='file',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_category', to='dlfile.file_category'),
        ),
    ]