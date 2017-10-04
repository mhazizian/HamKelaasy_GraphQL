from __future__ import unicode_literals

import random

from django.db import models
from django.utils.crypto import get_random_string


class Temp_phone_number(models.Model):
    phone_number = models.CharField('phone', max_length=12)
    code = models.CharField('security code', max_length=6)

    # will be sent to client when validating phone number
    validator = models.CharField('phone number validator', max_length=12)

    is_validated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.code = str(random.randint(10000, 99999))
            self.validator = get_random_string(length=10)
        super(Temp_phone_number, self).save(args, kwargs)

    def __unicode__(self):
        return self.phone_number
