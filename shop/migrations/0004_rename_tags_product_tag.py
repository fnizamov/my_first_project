# Generated by Django 4.1.3 on 2022-11-04 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_rename_tag_product_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='tags',
            new_name='tag',
        ),
    ]
