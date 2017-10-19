from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from core.utilz import pretty_past_time, pretty_remaining_time, to_shamsi_date


class Task(models.Model):
    kelaas = models.ForeignKey('Kelaas', related_name="in_progress_tasks", on_delete=models.CASCADE)
    student = models.ForeignKey('Person', related_name="tasks", on_delete=models.CASCADE)

    body = models.CharField('task body', max_length=1000)
    create_date = models.DateTimeField('task creation date', default=timezone.now)
    due_date = models.DateTimeField('task due date', null=True, default=None)

    is_done = models.BooleanField(default=False)

    @property
    def time_passed(self):
        delta = timezone.now() - self.create_date
        return pretty_past_time(delta)

    @property
    def shamsi_date(self):
        return to_shamsi_date(self.create_date)

    @property
    def remaining_time(self):
        if self.due_date:
            if self.due_date < timezone.now():
                return "time's up!!"
            delta = self.due_date - timezone.now()
            return pretty_remaining_time(delta)

    def __unicode__(self):
        return self.body
