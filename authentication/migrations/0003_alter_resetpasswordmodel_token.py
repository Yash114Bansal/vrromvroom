# Generated by Django 3.2.20 on 2024-01-01 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_resetpasswordmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resetpasswordmodel',
            name='token',
            field=models.CharField(max_length=100),
        ),
    ]
