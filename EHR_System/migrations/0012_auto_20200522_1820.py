# Generated by Django 3.0.4 on 2020-05-22 18:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('EHR_System', '0011_auto_20200522_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient_demographics',
            name='date_of_birth',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
