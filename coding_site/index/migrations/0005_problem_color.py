# Generated by Django 3.1.2 on 2021-05-27 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0004_auto_20210521_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='color',
            field=models.CharField(default='none', max_length=10),
        ),
    ]