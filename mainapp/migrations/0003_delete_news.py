# Generated by Django 4.1.1 on 2022-10-08 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0002_alter_news_options"),
    ]

    operations = [
        migrations.DeleteModel(
            name="News",
        ),
    ]
