# Generated by Django 3.2.8 on 2021-10-28 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AuthApp', '0004_advisor_booking_ad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advisor_booking',
            name='ad',
        ),
        migrations.AddField(
            model_name='advisor_booking',
            name='advisors',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='AuthApp.advisor'),
            preserve_default=False,
        ),
    ]
