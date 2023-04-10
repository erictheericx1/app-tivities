# Generated by Django 4.1.7 on 2023-04-10 08:33

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_wish_delete_inter_alter_useractivity_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='all_interests',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, default=('Art', 'Music', 'Sightseeing', 'Shopping', 'Restaurants', 'Bars', 'Events', 'Outdoor Recreation', 'History', 'Nature', 'Education', 'Fitness', 'Travel', 'Books', 'Photography', 'Theater', 'Architecture', 'Cuisine', 'Local Culture', 'Street Markets', 'Museums', 'Urban Exploration', 'City Parks', 'Public Transportation'), null=True, size=None),
        ),
    ]