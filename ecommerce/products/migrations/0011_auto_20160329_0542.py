# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20160329_0541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(to='products.Category', blank=True),
        ),
        migrations.AlterField(
            model_name='variation',
            name='image',
            field=models.ImageField(upload_to=products.models.image_upload_to),
        ),
    ]
