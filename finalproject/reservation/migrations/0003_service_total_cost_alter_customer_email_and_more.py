# Generated by Django 5.0.6 on 2024-05-27 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_servicetype_remove_timeslot_duration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='reservationstatus',
            name='status',
            field=models.IntegerField(choices=[(1, 'Reserved'), (2, 'Not Reserved')], default=2),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='name',
            field=models.CharField(max_length=40),
        ),
    ]
