# Generated by Django 4.1.3 on 2023-08-31 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('util', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumo',
            name='ultimoMes',
            field=models.IntegerField(default=0),
        ),
    ]