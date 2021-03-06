# Generated by Django 3.0.4 on 2020-05-20 02:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EHR_System', '0008_auto_20200520_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phys_exam',
            name='abdomen_desc',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='phys_exam',
            name='chest_desc',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='phys_exam',
            name='extremities_desc',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='phys_exam',
            name='formulation',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='phys_exam',
            name='genitalia_desc',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='phys_exam',
            name='heart',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='EHR_System.Phys_Exam_Heart'),
        ),
        migrations.AlterField(
            model_name='phys_exam',
            name='impression',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='phys_exam',
            name='lymph_nodes_desc',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='phys_exam',
            name='neurological_desc',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='phys_exam',
            name='pelvic_desc',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='phys_exam',
            name='plan',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='phys_exam',
            name='rectal_desc',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='phys_exam',
            name='vitals',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='EHR_System.Phys_Exam_Vitals'),
        ),
    ]
