from wagtail.core import blocks
from wagtail.core.blocks import CharBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailvideos.blocks import VideoChooserBlock

from django.db import models
from embed_video.fields import EmbedVideoField


#Original pet
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

    
# blocks.py
#class VideoBlock(blocks.StructBlock):
    """Only used for Video Card modals."""
#    video = EmbedBlock() # <-- the part we need

#    class Meta:
#        template = "cms/video_card_block.html"
#        icon = "media"
#        label = "Embed Video"


#Original Pet
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
       template = "streams/video_block.html"
       icon = 'media'
       label = 'YouTube Video'



class VideoBlock(blocks.StructBlock):
    video_server = VideoChooserBlock(label=("Video"))
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
        label = 'Server Video'  


#class MyVideoBlock(blocks.StreamBlock):
#    '''rich text'''
#title = blocks.CharBlock(required=True, help_text="Add your Title")
#texts = blocks.TextBlock(required=True, help_text="Add your additional text")
#embed = EmbedBlock()

#class Meta:
#    template = "streams/video_block.html"
#    icon = "edit"
#    label = "Full Rich Text"      



