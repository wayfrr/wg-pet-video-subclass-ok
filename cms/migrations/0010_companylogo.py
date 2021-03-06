# Generated by Django 3.2.7 on 2021-10-10 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('cms', '0009_auto_20211005_2324'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyLogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('logo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.image')),
            ],
        ),
    ]
