# Generated by Django 3.2.6 on 2021-11-04 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0041_field_dependencies'),
    ]

    operations = [
        migrations.AddField(
            model_name='formulafield',
            name='array_formula_type',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='formulafield',
            name='formula_type',
            field=models.TextField(choices=[('invalid', 'invalid'), ('text', 'text'), ('char', 'char'), ('date_interval', 'date_interval'), ('date', 'date'), ('boolean', 'boolean'), ('number', 'number'), ('array', 'array')], default='invalid'),
        ),
    ]
