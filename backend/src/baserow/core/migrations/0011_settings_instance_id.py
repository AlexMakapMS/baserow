# Generated by Django 3.2.6 on 2021-10-07 19:26

import secrets

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_fix_trash_constraint"),
    ]

    operations = [
        migrations.AddField(
            model_name="settings",
            name="instance_id",
            field=models.SlugField(default=secrets.token_urlsafe),
        ),
    ]
