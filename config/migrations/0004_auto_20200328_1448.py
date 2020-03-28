# Generated by Django 3.0.4 on 2020-03-28 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0003_auto_20200328_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='holiday',
            name='skipped_for_fine',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='lendingsettings',
            name='hand_in_days',
            field=models.IntegerField(default=1),
        ),
    ]