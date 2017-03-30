# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_code',
            field=models.DecimalField(default=1, max_digits=8, decimal_places=0),
            preserve_default=False,
        ),
    ]
