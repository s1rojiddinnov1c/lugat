# Generated by Django 5.0.1 on 2024-01-31 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_category_tag_news_category_news_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='tag',
            field=models.ManyToManyField(related_name='news_category', to='news.tag'),
        ),
    ]
