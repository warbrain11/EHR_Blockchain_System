# Generated by Django 3.0.4 on 2020-07-09 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain', '0003_auto_20200529_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verification',
            field=models.FileField(null=True, upload_to='uploads/verification', verbose_name='verification'),
        ),
    ]
