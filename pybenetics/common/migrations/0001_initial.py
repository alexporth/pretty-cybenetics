# Generated by Django 4.2.6 on 2023-10-07 18:37

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("url", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="EfficiencyCertification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=20)),
                ("image", models.ImageField(upload_to="")),
                ("value", models.IntegerField(default=0)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NoiseCertification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=20)),
                ("image", models.ImageField(upload_to="")),
                ("value", models.IntegerField(default=0)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
