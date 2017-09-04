# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.models.post import Post
from django.db import models


class Kelaas_post(Post):
    files = models.ManyToManyField('File', blank=True)

    def save(self, *args, **kwargs):
        self.type = 'Kelaas_post'
        super(Kelaas_post, self).save(args, kwargs)