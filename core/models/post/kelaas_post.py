# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.models.post import Post, KELAAS_POST_KEY_WORD
from django.db import models


class Kelaas_post(Post):
    files = models.ManyToManyField('File', blank=True)

    def save(self, *args, **kwargs):
        self.type = KELAAS_POST_KEY_WORD
        super(Kelaas_post, self).save(args, kwargs)

    def delete(self, *args, **kwargs):
        for post_file in self.files.all():
            post_file.delete()
        super(Kelaas_post, self).delete(*args, **kwargs)


    def __unicode__(self):
        return unicode(self.title) + unicode(self.description)