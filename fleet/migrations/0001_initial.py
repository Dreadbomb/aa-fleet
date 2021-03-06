# Generated by Django 2.2.12 on 2020-06-13 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Fleet",
            fields=[
                ("fleet_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("fleet_commander_id", models.BigIntegerField()),
                ("created_at", models.DateTimeField()),
                ("motd", models.CharField(max_length=4000)),
                ("is_free_move", models.BooleanField()),
            ],
            options={
                "permissions": (
                    ("fleet_access", "Can access this app"),
                    ("manage", "Can Manage Fleets"),
                ),
                "default_permissions": (),
            },
        ),
    ]
