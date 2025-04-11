# Generated by Django 5.2 on 2025-04-11 01:32

import apps.venue.constants
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0005_city_description'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='price',
            name='venue',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prices', to='venue.venuemodel'),
        ),
        migrations.AlterField(
            model_name='venueimages',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='venue.venuemodel'),
        ),
        migrations.AlterField(
            model_name='venuemodel',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='venues', to='venue.city'),
        ),
        migrations.AlterField(
            model_name='venuemodel',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='BookingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_people', models.PositiveIntegerField(default=0)),
                ('meal_type', models.CharField(choices=apps.venue.constants.FoodType.choices, default=apps.venue.constants.FoodType['VEG'], max_length=20)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to=settings.AUTH_USER_MODEL)),
                ('venue', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to='venue.venuemodel')),
            ],
        ),
    ]
