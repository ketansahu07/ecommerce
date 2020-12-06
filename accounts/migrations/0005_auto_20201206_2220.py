# Generated by Django 3.0.5 on 2020-12-06 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20201206_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False, help_text='Designates wherther the user is verified or not.', verbose_name='Verified'),
        ),
    ]
