# Generated by Django 3.2.5 on 2022-05-13 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0003_auto_20220513_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='shop_description',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
