# Generated by Django 5.1.7 on 2025-03-19 07:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0004_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='realestate.agent'),
        ),
    ]
