from __future__ import unicode_literals

import random

from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string


class Temp_phone_number(models.Model):
    phone_number = models.CharField('phone', max_length=15, primary_key=True)
    last_send_sms_time = models.DateTimeField('last sent sms time', default=timezone.now)

    code = models.CharField('security code', max_length=6)
    # will be sent to client when validating phone number
    validator = models.CharField('phone number validator', max_length=30)

    is_validated = models.BooleanField(default=False)
    is_registered = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randint(10000, 99999))
            self.validator = get_random_string(length=29)
        super(Temp_phone_number, self).save(args, kwargs)

    def re_init(self):
        self.code = str(random.randint(10000, 99999))
        self.validator = get_random_string(length=29)
        self.is_validated = False
        self.last_send_sms_time = timezone.now()
        self.save()

    def __unicode__(self):
        return self.phone_number
