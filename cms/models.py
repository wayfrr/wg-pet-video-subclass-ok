from django.db import models
from wagtail.core import blocks
from django import forms
from wagtail.core.models import Page
from modelcluster.fields import ParentalManyToManyField
from .blocks import InlineImageBlock,InlineVideoBlock, VideoBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtailcodeblock.blocks import CodeBlock
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet




# Create your models here.
#Categories Snippet


@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name

    class Meta:  # noqa
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class CategoryPage(Page):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='categorypages')
    intro = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+'
    )
    caption = models.CharField(blank=True, null=True, max_length=255)

    def articlepages(self):
        return self.category.articlepages.live().order_by('-first_published_at')

    content_panels = Page.content_panels + [
        SnippetChooserPanel('category'),
        FieldPanel('intro', classname='full'),
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]



class ArticlePage(Page):

    template = "cms/article_page.html"

    intro = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+', verbose_name=("Image")
    )
    categories = ParentalManyToManyField(Category, blank=True, related_name='articlepages', verbose_name=("Categories"))
    
    featured = models.BooleanField(default=False)
    body = StreamField([
        ('paragraph', blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'h5', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'image', 'code', 'blockquote'])),
        ('code', CodeBlock(label=("Code"))),
        ('image', InlineImageBlock()),
        
        ('video', InlineVideoBlock()),

        ('video_server', VideoBlock()),
        
        
    ])

    def categorypages(self):
        return CategoryPage.objects.filter(category__in=self.categories.all())



    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        FieldPanel('featured'),
        ImageChooserPanel('image'),
        
        StreamFieldPanel('body'),
        
    ]




class CategoryIndexPage(Page):
    intro = RichTextField(blank=True)

    # Specifies that only ThemePage objects can live under this index page
    subpage_types = ['CategoryPage']
    parent_page_types = ['home.HomePage']

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]


class ArticleIndexPage(Page):
    intro = RichTextField(blank=True)

    # Specifies that only ArticlePage objects can live under this index page
    subpage_types = ['ArticlePage','VideoBlogPage','CategoryIndexPage']

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
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        StreamFieldPanel("body"),
    ]

    