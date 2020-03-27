# Generated by Django 3.0.3 on 2020-03-20 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0007_publication_location'),
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LendingSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term_for_inactive', models.IntegerField()),
                ('term_for_active', models.IntegerField()),
                ('borrow_money_inactive', models.IntegerField()),
                ('borrow_money_active', models.IntegerField()),
                ('item_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='works.ItemType')),
            ],
        ),
    ]