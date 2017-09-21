from __future__ import unicode_literals

from .person import Person

TEACHER_KEY_WORD = "teacher"


class Teacher(Person):

    def save(self, *args, **kwargs):
        self.type = TEACHER_KEY_WORD
        if not self.profile_pic:
            self.profile_pic.name = 'teacher.svg'
        super(Teacher, self).save(args, kwargs)

    def __unicode__(self):
        return "teacher: " + unicode(self.last_name)
