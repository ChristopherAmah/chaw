# Generated by Django 4.0.6 on 2022-09-16 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_shopcart_c_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopcart',
            name='c_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
