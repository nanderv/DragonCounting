# Generated by Django 3.0.3 on 2020-02-20 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('comment', models.CharField(max_length=255)),
                ('old_id', models.IntegerField()),
                ('is_alias_of', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='works.Creator')),
            ],
        ),
        migrations.CreateModel(
            name='CreatorRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('sub_title', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=64)),
                ('is_translated', models.BooleanField()),
                ('original_title', models.CharField(max_length=255)),
                ('original_subtitle', models.CharField(max_length=255)),
                ('original_language', models.CharField(max_length=64)),
                ('hidden', models.BooleanField()),
                ('date_added', models.DateField()),
                ('comment', models.CharField(max_length=1024)),
                ('internal_comment', models.CharField(max_length=1024)),
                ('signature_fragment', models.CharField(max_length=64)),
                ('isbn', models.CharField(max_length=64)),
                ('old_id', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('work_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='works.Work')),
            ],
            bases=('works.work',),
        ),
        migrations.CreateModel(
            name='SubWork',
            fields=[
                ('work_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='works.Work')),
            ],
            bases=('works.work',),
        ),
        migrations.CreateModel(
            name='CreatorToWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='works.Creator')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='works.CreatorRole')),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='works.Work')),
            ],
        ),
        migrations.CreateModel(
            name='WorkInPublication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_in_publication', models.IntegerField()),
                ('display_number_in_publication', models.CharField(max_length=64)),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='works.Publication')),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='works.SubWork')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('old_id', models.IntegerField()),
                ('sticker_code', models.CharField(max_length=64)),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='works.Publication')),
            ],
        ),
    ]