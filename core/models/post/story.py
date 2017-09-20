# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from Hamkelaasy_graphQL import settings
from core.models.post import Post
from django.db import models

STORY_KEY_WORD = 'Story'


class Story(Post):
    story_pic = models.ForeignKey('File', blank=True, default=None, null=True)
    likes = models.ManyToManyField('Person')

    def save(self, *args, **kwargs):
        self.type = 'Story'
        super(Story, self).save(args, kwargs)

    @property
    def pic(self):
        if self.story_pic:
            return settings.SERVER_ADDR[:-1] + self.story_pic.url

    @property
    def like_count(self):
        return self.likes.count()
