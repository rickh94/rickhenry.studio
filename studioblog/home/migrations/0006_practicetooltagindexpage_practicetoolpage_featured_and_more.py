# Generated by Django 4.2.6 on 2023-10-10 22:14

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):
    dependencies = [
        ("taggit", "0005_auto_20220424_2025"),
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("home", "0005_practicetoolindexpage_practicetoolpage"),
    ]

    operations = [
        migrations.CreateModel(
            name="PracticeToolTagIndexPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.AddField(
            model_name="practicetoolpage",
            name="featured",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="PracticeToolTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "content_object",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tagged_items",
                        to="home.practicetoolpage",
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_items",
                        to="taggit.tag",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AlterField(
            model_name="practicetoolpage",
            name="tags",
            field=models.ManyToManyField(blank=True, to="home.practicetooltag"),
        ),
    ]
