# Generated by Django 4.2.1 on 2023-05-15 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_alter_profile_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='otp',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
