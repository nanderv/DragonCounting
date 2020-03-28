# Generated by Django 3.0.4 on 2020-03-28 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_auto_20200304_1615'),
        ('lendings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='reserved_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reservation_action_by', to='members.Member'),
        ),
    ]