# Generated by Django 3.0.4 on 2020-09-29 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0004_register'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='email',
            field=models.CharField(default='a', max_length=128),
            preserve_default=False,
        ),
    ]
