# Generated by Django 2.2.12 on 2020-06-13 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupmanagement', '0013_fix_requestlog_date_field'),
        ('fleet', '0002_fleet_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='fleet',
            name='groups',
            field=models.ManyToManyField(help_text='Group listed here will be able to join the fleet', related_name='restricted_groups', to='groupmanagement.AuthGroup'),
        ),
    ]