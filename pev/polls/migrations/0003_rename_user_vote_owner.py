# Generated by Django 4.2.6 on 2023-11-06 03:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0002_poll_updated_at"),
    ]

    operations = [
        migrations.RenameField(
            model_name="vote",
            old_name="user",
            new_name="owner",
        ),
    ]
