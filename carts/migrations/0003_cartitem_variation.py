# Generated by Django 3.1 on 2023-11-21 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_variation'),
        ('carts', '0002_auto_20231117_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variation',
            field=models.ManyToManyField(blank=True, to='store.Variation'),
        ),
    ]
