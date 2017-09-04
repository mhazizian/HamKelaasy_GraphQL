# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.models.post import Post
from django.db import models

KELAAS_POST_KEY_WORD = 'Kelaas_post'


class Kelaas_post(Post):
    files = models.ManyToManyField('File', blank=True)

    def save(self, *args, **kwargs):
        self.type = KELAAS_POST_KEY_WORD
        super(Kelaas_post, self).save(args, kwargs)
