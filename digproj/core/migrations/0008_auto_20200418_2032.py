# Generated by Django 2.2.4 on 2020-04-18 20:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_persona_registerdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='registerdate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
