# Generated by Django 4.2.1 on 2023-05-29 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_bids'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='isactive',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
