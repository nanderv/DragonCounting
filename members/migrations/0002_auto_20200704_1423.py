# Generated by Django 3.0.4 on 2020-07-04 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'permissions': [('committee_update', 'Can update committee')]},
        ),
    ]
