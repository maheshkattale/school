# Generated by Django 5.0.6 on 2024-05-29 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FeesMaster', '0007_alter_studentfeeslog_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentfeeslog',
            name='payment_type',
        ),
        migrations.AlterField(
            model_name='studentfeeslog',
            name='termid',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
