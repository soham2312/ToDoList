# Generated by Django 4.2.1 on 2023-05-11 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_profile_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]