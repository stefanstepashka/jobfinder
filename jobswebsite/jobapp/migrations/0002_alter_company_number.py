# Generated by Django 4.1.6 on 2023-02-19 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='number',
            field=models.IntegerField(),
        ),
    ]
