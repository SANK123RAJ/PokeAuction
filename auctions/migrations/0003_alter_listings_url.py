# Generated by Django 4.2.1 on 2023-05-28 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_listings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='url',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]