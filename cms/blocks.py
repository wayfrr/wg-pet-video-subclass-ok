from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core import blocks
from wagtail.core.blocks import CharBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

from wagtail.core.models import Page

import re
from django import template




class InlineImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(label=("Image"))
    caption = CharBlock(required=False, label=("Caption"))
    float = blocks.ChoiceBlock(
        required=False,
        choices=[('right', ("Right")), ('left', ("Left")), ('center', ("Center"))],
        default='right',
        label=("Float"),
    )
    size = blocks.ChoiceBlock(
        required=False,
        choices=[('small', ("Small")), ('medium', ("Medium")), ('large', ("Large"))],
        default='small',
        label=("Size"),
    )

    class Meta:
        icon = 'image'


class InlineVideoBlock(blocks.StructBlock):
    video = EmbedBlock(label=("Video"))
    caption = CharBlock(required=False, label=("Caption"))
    float = blocks.ChoiceBlock(
        required=False,
        choices=[('right', ("Right")), ('left', ("Left")), ('center', ("Center"))],
        default='right',
        label=("Float"),
    )
    size = blocks.ChoiceBlock(
        required=False,
        choices=[('small', ("Small")), ('medium', ("Medium")), ('large', ("Large"))],
        default='small',
        label=("Size"),
    )

    class Meta:
        icon = 'media'



    