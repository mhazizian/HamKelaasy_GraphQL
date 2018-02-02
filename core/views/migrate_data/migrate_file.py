# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib

import requests
import time

import core.services as services
from django.db import connection

from core.utilz import hash_password
import json

from core.models import *

from django.http import HttpResponse


def migrate_file(request):
    res = []
    for file in File.objects.all():
        if not file.link:
            continue

        obj = {
            "uuid": file.uuid,
            "link": file.link,
            "klass_id": file.klass,
            "owner_id": file.owner_id,
            "create_date": int(time.mktime(file.create_date.timetuple())),
            "is_optimized": file.is_optimized,
            "filesize": file.filesize,
            "md5sum": file.md5sum,
            "meta": file.meta,
            "orig_name": file.title

        }
        res.append(obj)

    return HttpResponse(json.dumps(res))
