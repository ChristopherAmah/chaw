# Generated by Django 4.0.6 on 2022-08-05 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techbro', '0007_dish_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='description',
            field=models.TextField(),
        ),
    ]
