# Generated by Django 5.0.1 on 2024-01-11 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_cart_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]