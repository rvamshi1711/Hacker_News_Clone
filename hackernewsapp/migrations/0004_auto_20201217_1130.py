# Generated by Django 3.1.3 on 2020-12-17 06:00

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hackernewsapp', '0003_auto_20201107_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='Description'),
        ),
    ]