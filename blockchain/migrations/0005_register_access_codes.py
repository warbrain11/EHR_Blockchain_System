# Generated by Django 3.0.4 on 2020-07-10 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain', '0004_user_verification'),
    ]

    operations = [
        migrations.CreateModel(
            name='Register_Access_Codes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=65, null=True)),
            ],
        ),
    ]
