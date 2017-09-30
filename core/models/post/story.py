# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.models.post import Post, STORY_KEY_WORD
from django.db import models


class Story(Post):
    story_pic = models.ForeignKey('File', blank=True, default=None, null=True)
    likes = models.ManyToManyField('Person')

    def save(self, *args, **kwargs):
        self.type = STORY_KEY_WORD
        super(Story, self).save(args, kwargs)

    def delete(self, *args, **kwargs):
        if self.story_pic:
            self.story_pic.delete()
        super(Story, self).delete(*args, **kwargs)

    @property
    def pic(self):
        if self.story_pic:
            return self.story_pic.url

    @property
    def like_count(self):
        return self.likes.count()

    def __unicode__(self):
        return unicode(self.title) + unicode(self.description)
