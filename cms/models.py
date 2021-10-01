from django.db import models
from wagtail.core import blocks

from wagtail.core.models import Page

from .blocks import InlineImageBlock, InlineVideoBlock 
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField

# Create your models here.


class ArticlePage(Page):

    template = "cms/article_page.html"

    intro = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+', verbose_name=("Image")
    )
    
    featured = models.BooleanField(default=False)
    body = StreamField([
        ('paragraph', blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'h5', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'image', 'code', 'blockquote'])),
        
        ('image', InlineImageBlock()),
        ('video', InlineVideoBlock()),
        
        
    ])

    

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('featured'),
        ImageChooserPanel('image'),
        
        StreamFieldPanel('body'),
        
    ]


class ArticleIndexPage(Page):
    intro = RichTextField(blank=True)

    # Specifies that only ArticlePage objects can live under this index page
    subpage_types = ['ArticlePage','VideoBlogPage']

    # A method to access and reorder the children of the page (i.e. ArticlePage objects)
    def articlepages(self):
        return ArticlePage.objects.child_of(self).live().order_by('-first_published_at')

    def featured_articlepages(self):
        return self.articlepages().filter(featured=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]


# First subclassed page-worked successfully
class VideoBlogPage(ArticlePage):
    """A video subclassed page."""

    template = "cms/video_blog_page.html"

    youtube_video_id = models.CharField(max_length=30)

    content_panels = Page.content_panels + [
        
        FieldPanel("youtube_video_id"),
        StreamFieldPanel("body"),
    ]