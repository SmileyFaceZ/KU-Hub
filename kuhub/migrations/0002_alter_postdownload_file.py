# Generated by Django 4.2.7 on 2023-11-25 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kuhub", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="postdownload",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
    ]