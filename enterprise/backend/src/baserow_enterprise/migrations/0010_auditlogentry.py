# Generated by Django 3.2.13 on 2022-12-16 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("baserow_enterprise", "0009_roleassignment_subject_and_scope_uniqueness"),
    ]

    operations = [
        migrations.CreateModel(
            name="AuditLogEntry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("event_type", models.CharField(db_index=True, max_length=32)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("ip_address", models.GenericIPAddressField(null=True)),
                ("user_id", models.PositiveIntegerField(db_index=True, null=True)),
                (
                    "user_email",
                    models.CharField(
                        blank=True, db_index=True, max_length=150, null=True
                    ),
                ),
                ("group_id", models.PositiveIntegerField(db_index=True, null=True)),
                (
                    "group_name",
                    models.CharField(
                        blank=True, db_index=True, max_length=160, null=True
                    ),
                ),
                ("data", models.JSONField(null=True)),
            ],
            options={
                "ordering": ["-timestamp"],
            },
        ),
    ]