# Generated by Django 3.0.4 on 2020-05-25 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EHR_System', '0013_auto_20200523_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergency_contacts',
            name='primary_phone',
            field=models.CharField(max_length=13),
        ),
    ]
