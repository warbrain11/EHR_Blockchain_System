# Generated by Django 3.0.4 on 2020-07-09 21:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('EHR_System', '0016_patient_authorized_viewers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='authorized_viewers',
        ),
        migrations.AddField(
            model_name='patient',
            name='Users',
            field=models.ManyToManyField(related_name='Users', to=settings.AUTH_USER_MODEL),
        ),
    ]
