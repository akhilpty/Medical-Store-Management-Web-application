# Generated by Django 4.1.7 on 2023-06-13 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical_store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='count',
            field=models.IntegerField(null=True),
        ),
    ]
