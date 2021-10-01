from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.core.fields import RichTextField


class HomePage(Page):

    template = "home/home_page.html"
    max_count = 1
    intro = RichTextField(blank=True)
    article_section_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text=("Title to display above the article section"),
    )
    article_section_intro = RichTextField(blank=True)
    article_section = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=("Featured articles for the homepage"),
        verbose_name=("Article section"),
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
       
        MultiFieldPanel([
            FieldPanel('article_section_title'),
            FieldPanel('article_section_intro', classname='full'),
            PageChooserPanel('article_section'),
            ], heading=("Article section"), classname='collapsible'),
    ]
    
