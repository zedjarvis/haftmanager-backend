# Generated by Django 4.2 on 2023-04-30 23:50

import apps.accounts.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import imagekit.models.fields
import model_utils.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('website', models.URLField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('billing_address', models.CharField(blank=True, max_length=255)),
                ('shipping_address', models.CharField(blank=True, max_length=255)),
                ('logo', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=apps.accounts.models.account_directory_path)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('is_primary', models.BooleanField(default=False)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phones', to='accounts.account')),
            ],
            options={
                'verbose_name': 'Account Phone',
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('email_address', models.EmailField(max_length=255)),
                ('is_primary', models.BooleanField(default=False)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='accounts.account')),
            ],
            options={
                'verbose_name': 'Account Email',
            },
        ),
        migrations.CreateModel(
            name='AccountSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('currency', models.CharField(blank=True, max_length=128)),
                ('time_zone', models.CharField(blank=True, max_length=128)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
            options={
                'verbose_name_plural': 'Account Settings',
            },
        ),
        migrations.AddField(
            model_name='account',
            name='industry',
            field=models.ManyToManyField(to='accounts.industry'),
        ),
        migrations.AddConstraint(
            model_name='phone',
            constraint=models.UniqueConstraint(fields=('account', 'phone_number'), name='unique_account_phone_number'),
        ),
        migrations.AddConstraint(
            model_name='email',
            constraint=models.UniqueConstraint(fields=('account', 'email_address'), name='unique_account_email_address'),
        ),
    ]
