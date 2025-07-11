# Generated by Django 4.1.3 on 2024-04-29 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ClassMaster', '0001_initial'),
        ('SubjectMaster', '0001_initial'),
        ('TimeTableMaster', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True, null=True)),
                ('updatedAt', models.DateTimeField(auto_now_add=True, null=True)),
                ('createdBy', models.CharField(blank=True, max_length=255, null=True)),
                ('updatedBy', models.CharField(blank=True, max_length=255, null=True)),
                ('isActive', models.BooleanField(blank=True, default=True, null=True)),
                ('Date', models.DateField(blank=True, null=True)),
                ('start_time', models.CharField(max_length=255, null=True)),
                ('end_time', models.CharField(max_length=255, null=True)),
                ('TeacherId', models.CharField(blank=True, max_length=250, null=True)),
                ('school_code', models.CharField(blank=True, max_length=150, null=True)),
                ('ClassId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ClassMaster.class')),
                ('Day', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TimeTableMaster.days')),
                ('SubjectId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SubjectMaster.subject')),
            ],
            options={
                'ordering': ('-createdAt',),
                'abstract': False,
            },
        ),
    ]
