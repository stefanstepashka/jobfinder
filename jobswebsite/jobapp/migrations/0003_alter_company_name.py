# Generated by Django 4.1.6 on 2023-02-19 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0002_alter_company_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
