# Generated by Django 4.0.3 on 2022-04-15 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_user_full_name_remove_user_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='user_name',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]