# Generated by Django 4.2.6 on 2023-11-06 03:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0003_rename_user_vote_owner"),
    ]

    operations = [
        migrations.RenameField(
            model_name="vote",
            old_name="owner",
            new_name="user",
        ),
    ]
