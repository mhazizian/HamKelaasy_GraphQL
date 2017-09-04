# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.models.post import Post
from django.db import models

STORY_KEY_WORD = 'Story'

class Story(Post):
    story_pic = models.FileField('story pic', upload_to='story/%Y/%m/%d/', blank=True)

    @property
    def pic(self):
        return self.story_pic.url

    def save(self, *args, **kwargs):
        self.type = 'Story'
        super(Story, self).save(args, kwargs)
