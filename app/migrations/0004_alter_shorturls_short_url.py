# Generated by Django 4.2.7 on 2023-12-12 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_shorturls_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shorturls',
            name='short_url',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]