# Generated by Django 3.1.2 on 2021-05-21 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_auto_20210515_1408'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['tag_name']},
        ),
    ]
