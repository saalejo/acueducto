# Generated by Django 4.1.3 on 2022-12-07 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('util', '0007_alter_movimiento_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movimiento',
            options={'ordering': ['nitcte', '-codcon']},
        ),
    ]