from django.db import models
from wagtail.core import blocks
from django import forms
from wagtail.core.models import Page
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from .blocks import InlineImageBlock,InlineVideoBlock, VideoBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel,InlinePanel,MultiFieldPanel,PageChooserPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtailcodeblock.blocks import CodeBlock
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from django_extensions.db.fields import AutoSlugField
from modelcluster.models import ClusterableModel
from wagtail.core.models import Orderable
from django.utils.text import slugify



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



@register_snippet
class Menu(ClusterableModel):

    title = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='title', editable=True, help_text="Unique identifier of menu. Will be populated automatically from title of menu. Change only if needed.")

    panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('slug'),
        ], heading=("Menu")),
        InlinePanel('menu_items', label=("Menu Item"))
    ]

    def __str__(self):
        return self.title


class MenuItem(Orderable):
    menu = ParentalKey('Menu', related_name='menu_items', help_text=("Menu to which this item belongs"))
    title = models.CharField(max_length=50, help_text=("Title of menu item that will be displayed"))
    link_url = models.CharField(max_length=500, blank=True, null=True, help_text=("URL to link to, e.g. /accounts/signup (no language prefix, LEAVE BLANK if you want to link to a page instead of a URL)"))
    link_page = models.ForeignKey(
       Page, blank=True, null=True, related_name='+', on_delete=models.CASCADE, help_text=("Page to link to (LEAVE BLANK if you want to link to a URL instead)"),
    )
    title_of_submenu = models.CharField(
        blank=True, null=True, max_length=50, help_text=("Title of submenu (LEAVE BLANK if there is no custom submenu)")
    )
    icon = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
    )
    show_when = models.CharField(
        max_length=15,
        choices=[('always', ("Always")), ('logged_in', ("When logged in")), ('not_logged_in', ("When not logged in"))],
        default='always',
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('link_url'),
        PageChooserPanel('link_page'),
        FieldPanel('title_of_submenu'),
        ImageChooserPanel('icon'),
        FieldPanel('show_when'),
    ]

    @property
    def slug_of_submenu(self):
        # becomes slug of submenu if there is one, otherwise None
        if self.title_of_submenu:
            return slugify(self.title_of_submenu)
        return None

    def show(self, authenticated):
        return ((self.show_when == 'always')
                or (self.show_when == 'logged_in' and authenticated)
                or (self.show_when == 'not_logged_in' and not authenticated))


    
    def page(self):
        if self.link_page:
            return self.link_page
        
        return 'None'

    
    def url(self):
        if self.link_url:
            return '/'+ self.link_url
        elif self.link_page:
            return self.link_page.url
        return 'None'


    def __str__(self):
        return self.title