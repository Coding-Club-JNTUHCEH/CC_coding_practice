# Generated by Django 3.0.2 on 2021-05-18 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=32)),
                ('tag_title', models.CharField(default='did not set', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contestID', models.IntegerField()),
                ('index', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=50)),
                ('rating', models.IntegerField(default=0)),
                ('link', models.URLField()),
                ('tags', models.ManyToManyField(blank=True, related_name='Problme', to='index.Tag')),
            ],
            options={
                'unique_together': {('contestID', 'index')},
            },
        ),
    ]