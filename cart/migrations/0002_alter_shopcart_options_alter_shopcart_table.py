# Generated by Django 4.0.6 on 2022-08-31 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shopcart',
            options={'managed': True, 'verbose_name': 'Shopcart', 'verbose_name_plural': 'Shopcarts'},
        ),
        migrations.AlterModelTable(
            name='shopcart',
            table='shopcart',
        ),
    ]
