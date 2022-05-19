# Generated by Django 4.0.4 on 2022-05-18 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservoirs', '0003_alter_watersituation_reservoir'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='watersituation',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='watersituation',
            constraint=models.UniqueConstraint(fields=('date', 'reservoir_id'), name='water_situation_date_reservoir_id_key'),
        ),
    ]