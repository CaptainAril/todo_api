# Generated by Django 5.1.4 on 2025-01-21 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_alter_todo_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='priority',
            field=models.CharField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=1, max_length=9),
        ),
    ]
