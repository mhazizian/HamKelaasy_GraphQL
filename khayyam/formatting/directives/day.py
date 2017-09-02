# -*- coding: utf-8 -*-
from .base import Directive
from .persian import PersianNumberDirective
from khayyam.algorithms import get_days_in_jalali_year
from datetime import timedelta
__author__ = 'vahid'


class PersianDayDirective(PersianNumberDirective):
    """
    Representing a day in persian calendar.
    """

    def format(self, d):
        return super(PersianDayDirective, self).format(d.day)

    def post_parser(self, ctx, formatter):
        super(PersianDayDirective, self).post_parser(ctx, formatter)
        if self.name in ctx and ctx[self.name]:
            ctx['day'] = ctx[self.name]


class DayOfYearDirective(Directive):
    """
    Representing day of year.
    """

    def format(self, d):
        return '%.3d' % d.dayofyear()

    def post_parser(self, ctx, formatter):
        _dayofyear = ctx['dayofyear']
        if 'year' not in ctx:
            ctx['year'] = 1
        if 'month' in ctx:
            del ctx['month']
        if 'day' in ctx:
            del ctx['day']

        max_days = get_days_in_jalali_year(ctx['year'])
        if _dayofyear > max_days:
            raise ValueError(
                'Invalid dayofyear: %.3d for year %.4d. Valid values are: 1-%s' % (
                    _dayofyear,
                    ctx['year'],
                    max_days))
        from khayyam import JalaliDate
        d = JalaliDate(year=ctx['year']) + timedelta(days=_dayofyear-1)
        ctx.update(dict(
            month=d.month,
            day=d.day
        ))


class PersianDayOfYearDirective(PersianNumberDirective):
    """
    Representing day of year in persian.
    """

    def format(self, d):
        return super(PersianDayOfYearDirective, self).format(d.dayofyear())

    def post_parser(self, ctx, formatter):
        super(PersianDayOfYearDirective, self).post_parser(ctx, formatter)
        if self.name in ctx and ctx[self.name]:
            ctx['dayofyear'] = ctx[self.name]
