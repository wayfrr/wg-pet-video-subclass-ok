# Generated by Django 3.2.7 on 2021-09-29 17:08

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0062_comment_models_and_pagesubscription'),
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='article_section',
            field=models.ForeignKey(blank=True, help_text='Featured articles for the homepage', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.page', verbose_name='Article section'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='article_section_intro',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='article_section_title',
            field=models.CharField(blank=True, help_text='Title to display above the article section', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='intro',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
    ]
