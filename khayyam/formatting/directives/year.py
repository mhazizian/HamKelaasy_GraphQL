# -*- coding: utf-8 -*-
from .base import Directive
from .persian import PersianNumberDirective
__author__ = 'vahid'


class ShortYearDirective(Directive):
    """
    Representing 2 digits year format.

    """
    def format(self, d):
        return '%.2d' % (d.year % 100)

    def post_parser(self, ctx, formatter):
        from khayyam import JalaliDate
        ctx['year'] = int(JalaliDate.today().year / 100) * 100 + ctx['shortyear']


class PersianYearDirective(PersianNumberDirective):
    """
    Representing year in persian form.

    """

    def format(self, d):
        return super(PersianYearDirective, self).format(d.year)

    def post_parser(self, ctx, formatter):
        super(PersianYearDirective, self).post_parser(ctx, formatter)
        if self.name in ctx and ctx[self.name]:
            ctx['year'] = ctx[self.name]


class PersianShortYearDirective(PersianNumberDirective):
    """
    Representing 2 digits year in persian form.

    """

    def format(self, d):
        return super(PersianShortYearDirective, self).format(d.year % 100)

    def post_parser(self, ctx, formatter):
        super(PersianShortYearDirective, self).post_parser(ctx, formatter)
        if self.name in ctx and ctx[self.name] is not None:
            ctx['shortyear'] = ctx[self.name]
