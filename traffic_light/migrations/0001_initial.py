# Generated by Django 3.0.3 on 2020-09-10 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrafficLightStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_datetime', models.DateTimeField()),
                ('to_datetime', models.DateTimeField(blank=True, null=True)),
                ('open', models.BooleanField()),
            ],
        ),
    ]
