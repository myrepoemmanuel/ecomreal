# Generated by Django 3.2.5 on 2023-01-11 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0032_featuredproduct_mainccategory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='products',
            options={'verbose_name_plural': 'Products'},
        ),
    ]