# Generated by Django 3.2.5 on 2022-06-21 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FriendRequests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_one', models.CharField(blank=True, max_length=200, null=True)),
                ('user_two', models.CharField(blank=True, max_length=200, null=True)),
                ('state', models.BooleanField(default=False)),
            ],
        ),
    ]