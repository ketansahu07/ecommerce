# Generated by Django 3.0.5 on 2020-11-18 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='Line_item_total',
            new_name='line_item_total',
        ),
    ]
