# Generated by Django 4.1.7 on 2023-06-13 17:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical_store', '0002_medicine_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='medicine_expiry',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
