# Generated by Django 4.1.3 on 2024-04-28 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('util', '0002_lectura_lectura_anterior'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumo',
            name='observacion',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]