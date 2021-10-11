# Generated by Django 3.2.7 on 2021-10-11 06:47

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('django_comments_xtd', '0009_alter_blacklisteddomain_id'),
        ('cms', '0011_textpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomComment',
            fields=[
                ('xtdcomment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_comments_xtd.xtdcomment')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='customcomments', to='cms.articlepage')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
                'ordering': ('submit_date',),
                'permissions': [('can_moderate', 'Can moderate comments')],
                'abstract': False,
            },
            bases=('django_comments_xtd.xtdcomment',),
        ),
    ]
