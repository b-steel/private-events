# Generated by Django 3.1.4 on 2020-12-08 03:18

import apps.core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(validators=[apps.core.models.validate_not_past], verbose_name='event date'),
        ),
    ]
