# Generated by Django 3.2.5 on 2021-11-28 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20211128_0328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='customer',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
