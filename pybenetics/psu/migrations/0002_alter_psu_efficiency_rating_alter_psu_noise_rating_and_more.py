# Generated by Django 4.2.6 on 2023-10-09 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0004_alter_efficiencycertification_image_and_more"),
        ("psu", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="psu",
            name="efficiency_rating",
            field=models.ForeignKey(
                blank=True, on_delete=django.db.models.deletion.PROTECT, to="common.efficiencycertification"
            ),
        ),
        migrations.AlterField(
            model_name="psu",
            name="noise_rating",
            field=models.ForeignKey(
                blank=True, on_delete=django.db.models.deletion.PROTECT, to="common.noisecertification"
            ),
        ),
        migrations.RemoveField(
            model_name="psu",
            name="tags",
        ),
        migrations.AddField(
            model_name="psu",
            name="tags",
            field=models.ManyToManyField(to="psu.tag"),
        ),
    ]
