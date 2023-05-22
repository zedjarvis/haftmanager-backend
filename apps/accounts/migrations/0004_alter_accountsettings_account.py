# Generated by Django 4.2 on 2023-05-18 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_remove_account_level_remove_account_lft_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accountsettings",
            name="account",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="account_settings",
                to="accounts.account",
            ),
        ),
    ]