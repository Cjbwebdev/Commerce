# Generated by Django 5.2 on 2025-05-28 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_alter_listing_imageurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='imageUrl',
            field=models.URLField(max_length=1000, null=True),
        ),
    ]
