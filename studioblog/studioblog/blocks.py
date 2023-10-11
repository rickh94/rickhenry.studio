import random

from wagtail.blocks import IntegerBlock, StructBlock, TextBlock
from wagtail.documents.blocks import DocumentChooserBlock


def random_id():
    return random.randint(10000, 99999)


class ABCBlock(StructBlock):
    notes = TextBlock(required=True)
    id = IntegerBlock(required=True, default=random_id)

    class Meta:
        template = "studioblog/blocks/abc_block.html"
        icon = "clef_staff"


class AudioBlock(StructBlock):
    recording = DocumentChooserBlock(required=True)

    class Meta:
        template = "studioblog/blocks/audio_block.html"
        icon = "media"
