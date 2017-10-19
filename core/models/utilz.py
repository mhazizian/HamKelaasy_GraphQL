# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import jdatetime as jdatetime

def to_shamsi_date(time):
    year, month, day = jdatetime.GregorianToJalali(time.year, time.month, time.day).getJalaliList()
    return jdatetime.datetime(year, month, day, time.hour, time.minute, time.second).strftime("%a, %d %b %Y %H:%M")


def pretty_past_time(diff):
    """
    Get a delta  datetime object and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "همین الان"
        if second_diff < 60:
            return str(second_diff) + " ثانیه پیش"
        if second_diff < 120:
            return "یک دقیقه پیش"
        if second_diff < 3600:
            return str(second_diff / 60) + " دقیقه پیش"
        if second_diff < 7200:
            return "یک ساعت پیش"
        if second_diff < 86400:
            return str(second_diff / 3600) + " ساعت پیش"
    if day_diff == 1:
        return "دیروز"
    if day_diff < 7:
        return str(day_diff) + " روز پیش"
    if day_diff < 31:
        return str(day_diff / 7) + " هفته پیش"
    if day_diff < 365:
        return str(day_diff / 30) + " ماه پیش"
    return str(day_diff / 365) + " سال پیش"


def pretty_remaining_time(diff):
    """
    Get a delta  datetime object and return a
    pretty string like 'an hour remains', '1 day', '3 months',
    'just now', etc
    """
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "همین الان"
        if second_diff < 60:
            return str(second_diff) + " ثانیه مانده"
        if second_diff < 120:
            return "یک دقیقه مانده"
        if second_diff < 3600:
            return str(second_diff / 60) + " دقیقه مانده"
        if second_diff < 7200:
            return "یک ساعت مانده"
        if second_diff < 86400:
            return str(second_diff / 3600) + " ساعت مانده"
    if day_diff == 1:
        return "فردا"
    if day_diff < 7:
        return str(day_diff) + " روز مانده"
    if day_diff < 31:
        return str(day_diff / 7) + " هفته مانده"
    if day_diff < 365:
        return str(day_diff / 30) + " ماه مانده"
    return str(day_diff / 365) + " سال مانده"
