# Generated by Django 3.0.2 on 2021-06-14 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_userprofile_sloved_problems_count'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'ordering': ['-rating', 'sloved_problems_count']},
        ),
    ]
