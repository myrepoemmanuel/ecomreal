# Generated by Django 3.2.5 on 2022-03-12 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_featuredproduct_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='price',
            field=models.FloatField(),
        ),
    ]