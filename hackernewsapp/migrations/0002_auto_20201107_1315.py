# Generated by Django 3.1.3 on 2020-11-07 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hackernewsapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='content',
            new_name='your_comment',
        ),
    ]
