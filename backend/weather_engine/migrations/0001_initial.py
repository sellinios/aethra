# Generated by Django 5.1.2 on 2024-10-12 15:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GFSParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('level_layer', models.CharField(max_length=255)),
                ('parameter', models.CharField(max_length=255)),
                ('forecast_valid', models.CharField(default='N/A', max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('enabled', models.BooleanField(default=True)),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'unique_together': {('number', 'level_layer', 'parameter')},
            },
        ),
    ]
