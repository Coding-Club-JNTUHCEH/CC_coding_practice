# Generated by Django 3.0.2 on 2021-06-14 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userprofile_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='sloved_problems_count',
            field=models.IntegerField(default=0),
        ),
    ]
