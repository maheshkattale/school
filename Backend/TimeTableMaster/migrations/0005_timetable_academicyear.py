# Generated by Django 4.1.3 on 2024-05-13 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SchoolMaster', '0004_school_school_logo'),
        ('TimeTableMaster', '0004_remove_timetable_date_remove_timetable_month_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='AcademicYear',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SchoolMaster.academicyear'),
        ),
    ]
