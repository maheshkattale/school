# Generated by Django 4.2.13 on 2024-06-05 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Parent_StudentMaster', '0006_alter_studentclasslog_exam'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentclasslog',
            old_name='exam',
            new_name='Exam',
        ),
    ]
