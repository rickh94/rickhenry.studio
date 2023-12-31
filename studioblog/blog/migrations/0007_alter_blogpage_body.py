# Generated by Django 4.2.6 on 2023-10-11 19:40

from django.db import migrations
import studioblog.blocks
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0006_alter_blogpage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("heading", wagtail.blocks.CharBlock(form_classname="title")),
                    ("paragraph", wagtail.blocks.RichTextBlock()),
                    ("image", wagtail.images.blocks.ImageChooserBlock()),
                    (
                        "abcnotes",
                        wagtail.blocks.StructBlock(
                            [
                                ("notes", wagtail.blocks.TextBlock(required=True)),
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
    ]
