# Generated by Django 3.0.4 on 2020-08-03 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0004_remove_series_book_code_extension'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='book_code_sortable',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
