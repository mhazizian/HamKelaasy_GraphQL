# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

KELAAS_POST_KEY_WORD = 'Kelaas_post'
STORY_KEY_WORD = 'Story'

from core.models.utilz import pretty_past_time
from khayyam import *


class Post(models.Model):
    title = models.CharField('post title', max_length=1000, null=True)
    description = models.CharField('post body', max_length=2000)
    create_date = models.DateTimeField('post creation date', default=timezone.now)
    type = models.CharField('post type', max_length=17, default='')

    kelaas = models.ForeignKey('Kelaas', related_name="posts", on_delete=models.CASCADE)
    owner = models.ForeignKey('Teacher', related_name="posts", on_delete=models.CASCADE)

    @property
    def shamsi_date(self):
        return JalaliDatetime(self.create_date).strftime(
            '%A %D %B %N  %h:%v')

    @property
    def time_passed(self):
        delta = timezone.now() - self.create_date
        return pretty_past_time(delta)

    @property
    def comment_count(self):
        return self.comments.count()

    def __unicode__(self):
        return unicode(self.title) + unicode(self.description)

    def delete(self, *args, **kwargs):
        for comment in self.comments.all():
            comment.delete()

        if self.type == STORY_KEY_WORD:
            self.story.delete()

        if self.type == KELAAS_POST_KEY_WORD:
            self.kelaas_post.delete()

