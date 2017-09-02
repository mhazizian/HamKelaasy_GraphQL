from __future__ import unicode_literals
from django.db import models


class Tag(models.Model):
    title = models.CharField('Tag name', max_length=100)

    def __unicode__(self):
        return self.title
