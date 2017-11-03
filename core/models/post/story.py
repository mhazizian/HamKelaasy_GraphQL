# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.models.post import Post, STORY_KEY_WORD
from django.db import models


class Story(Post):
    story_pic = models.ForeignKey('File', blank=True, default=None, null=True, related_name="story_picture")
    pics = models.ManyToManyField('File')
    likes = models.ManyToManyField('Person')

    def my_save(self):
        self.type = STORY_KEY_WORD
        self.save()

    def on_delete_story(self):
        if self.story_pic:
            self.story_pic.delete()

    @property
    def pic(self):
        if self.pics.count() != 0:
            return self.pics.first().url

        # if self.story_pic:
        #     return self.story_pic.url

    @property
    def like_count(self):
        return self.likes.count()

    def __unicode__(self):
        return unicode(self.title) + unicode(self.description)
