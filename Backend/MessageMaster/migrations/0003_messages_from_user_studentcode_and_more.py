# Generated by Django 5.0.6 on 2024-07-09 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MessageMaster', '0002_alter_messages_studentcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='from_user_studentcode',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='messages',
            name='to_user_studentcode',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
