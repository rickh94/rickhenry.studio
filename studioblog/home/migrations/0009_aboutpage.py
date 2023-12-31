# Generated by Django 4.2.6 on 2023-10-12 16:51

import django.db.models.deletion
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models

import studioblog.blocks


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("home", "0008_practicetooltag_practicetoolpage_tags"),
    ]

    operations = [
        migrations.CreateModel(
            name="AboutPage",
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
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            (
                                "heading",
                                wagtail.blocks.CharBlock(form_classname="title"),
                            ),
                            ("paragraph", wagtail.blocks.RichTextBlock()),
                            ("image", wagtail.images.blocks.ImageChooserBlock()),
                            (
                                "abcnotes",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "notes",
                                            wagtail.blocks.TextBlock(required=True),
                                        ),
                                        (
                                            "id",
                                            wagtail.blocks.IntegerBlock(
                                                default=studioblog.blocks.random_id,
                                                required=True,
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            (
                                "audio",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "recording",
                                            wagtail.documents.blocks.DocumentChooserBlock(
                                                required=True
                                            ),
                                        )
                                    ]
                                ),
                            ),
                        ],
                        blank=True,
                        use_json_field=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]
