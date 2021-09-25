# Generated by Django 3.2.6 on 2021-09-15 13:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0037_alter_exportjob_export_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="FormulaField",
            fields=[
                (
                    "field_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="database.field",
                    ),
                ),
                ("formula", models.TextField()),
                ("error", models.TextField(blank=True, null=True)),
                (
                    "formula_type",
                    models.TextField(
                        choices=[
                            ("invalid", "invalid"),
                            ("text", "text"),
                            ("boolean", "boolean"),
                            ("date", "date"),
                            ("number", "number"),
                            ("char", "char"),
                        ],
                        default="invalid",
                    ),
                ),
                (
                    "number_decimal_places",
                    models.IntegerField(
                        choices=[
                            (0, "1"),
                            (1, "1.0"),
                            (2, "1.00"),
                            (3, "1.000"),
                            (4, "1.0000"),
                            (5, "1.00000"),
                        ],
                        default=None,
                        help_text="The amount of digits allowed after the point.",
                        null=True,
                    ),
                ),
                (
                    "date_format",
                    models.CharField(
                        choices=[
                            ("EU", "European (D/M/Y)"),
                            ("US", "US (M/D/Y)"),
                            ("ISO", "ISO (Y-M-D)"),
                        ],
                        default=None,
                        help_text="EU (20/02/2020), US (02/20/2020) or ISO (2020-02-20)",
                        max_length=32,
                        null=True,
                    ),
                ),
                (
                    "date_include_time",
                    models.BooleanField(
                        default=None,
                        help_text="Indicates if the field also includes a time.",
                        null=True,
                    ),
                ),
                (
                    "date_time_format",
                    models.CharField(
                        choices=[("24", "24 hour"), ("12", "12 hour")],
                        default=None,
                        help_text="24 (14:30) or 12 (02:30 PM)",
                        max_length=32,
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("database.field",),
        ),
        migrations.RunSQL(
            (
                """
create or replace function try_cast_to_numeric(
    p_in text
)
    returns numeric(55, 5)
as
$$
begin
    begin
        return p_in::numeric(55, 5);
    exception when others then
        return 'NaN';
    end;
end;
$$
    language plpgsql;
"""
            ),
            ("DROP FUNCTION IF EXISTS try_cast_to_numeric(text);"),
        ),
        migrations.RunSQL(
            (
                """
create or replace function try_cast_to_date(
    p_in text,
    p_format text
)
    returns date
as
$$
begin
    begin
        return to_date(p_in, p_format);
    exception when others then
        return null;
    end;
end;
$$
    language plpgsql;
"""
            ),
            ("DROP FUNCTION IF EXISTS try_cast_to_date(text, text);"),
        ),
        migrations.RunSQL(
            (
                """
CREATE OR REPLACE FUNCTION DateDiff (units TEXT, start_t TIMESTAMP, end_t TIMESTAMP)
     RETURNS NUMERIC(50, 0) AS $$
   DECLARE
     diff_interval INTERVAL;
     diff NUMERIC(50, 0) = 0;
     years_diff NUMERIC(50, 0) = 0;
   BEGIN
     IF units IN ('yy', 'yyyy', 'year', 'mm', 'm', 'month') THEN
       years_diff = DATE_PART('year', end_t) - DATE_PART('year', start_t);

       IF units IN ('yy', 'yyyy', 'year') THEN
         -- SQL Server does not count full years passed (only difference between year parts)
         RETURN years_diff;
       ELSE
         -- If end month is less than start month it will subtracted
         RETURN years_diff * 12 + (DATE_PART('month', end_t) - DATE_PART('month', start_t));
       END IF;
     END IF;

     -- Minus operator returns interval 'DDD days HH:MI:SS'
     diff_interval = end_t - start_t;

     diff = diff + DATE_PART('day', diff_interval);

     IF units IN ('wk', 'ww', 'week') THEN
       diff = diff/7;
       RETURN diff;
     END IF;

     IF units IN ('dd', 'd', 'day') THEN
       RETURN diff;
     END IF;

     diff = diff * 24 + DATE_PART('hour', diff_interval);

     IF units IN ('hh', 'hour') THEN
        RETURN diff;
     END IF;

     diff = diff * 60 + DATE_PART('minute', diff_interval);

     IF units IN ('mi', 'n', 'minute') THEN
        RETURN diff;
     END IF;

     IF units IN ('s', 'ss', 'second') THEN
        RETURN diff * 60 + DATE_PART('second', diff_interval);
     END IF;

     RETURN 'NaN';
   END;
   $$ LANGUAGE plpgsql;
"""
            ),
            ("DROP FUNCTION IF EXISTS try_cast_to_date(text, text);"),
        ),
    ]
