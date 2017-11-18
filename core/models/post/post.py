# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from core.utilz import pretty_past_time, to_shamsi_date

KELAAS_POST_KEY_WORD = 'Kelaas_post'
STORY_KEY_WORD = 'Story'


class Post(models.Model):
    title = models.CharField('post title', max_length=1000, null=True)
    description = models.CharField('post body', max_length=2000)
    create_date = models.DateTimeField('post creation date', default=timezone.now)
    type = models.CharField('post type', max_length=17, default='')

    kelaas = models.ForeignKey('Kelaas', related_name="posts", on_delete=models.CASCADE)
    owner = models.ForeignKey('Teacher', related_name="posts", on_delete=models.CASCADE)

    seen = models.ManyToManyField('Person')

    @property
    def shamsi_date(self):
        return to_shamsi_date(self.create_date)

    @property
    def time_passed(self):
        delta = timezone.now() - self.create_date
        return pretty_past_time(delta)

    @property
    def comment_count(self):
        return self.comments.count()

    @property
    def seen_count(self):
        return self.seen.count()

    def __unicode__(self):
        return unicode(self.title) + unicode(self.description)

    def delete(self, *args, **kwargs):
        if self.type == STORY_KEY_WORD:
            self.story.on_delete_story()

        if self.type == KELAAS_POST_KEY_WORD:
            self.kelaas_post.on_delete_kelaas_post()

        super(Post, self).delete(*args, **kwargs)
