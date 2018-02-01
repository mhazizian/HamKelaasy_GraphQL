import json
import subprocess
import urllib

import requests
from django.core.management.base import BaseCommand
from os.path import join, basename, dirname, splitext
from uuid import uuid4

from Hamkelaasy_graphQL import settings
from core.models import File, Story, Kelaas_post

BACKTORY_AUTHENTICATION_ID = '5a3ba2f0e4b01a2811282807'
BACKTORY_AUTHENTICATION_MASTER_KEY = '058f04d8ea7546d6bfe99e49'
BACKTORY_AUTHENTICATION_CLIENT_KEY = '5a3ba2f0e4b0a3ac335b4fb4'
BACKTORY_API_SERVICE_PREFIX = 'https://api.backtory.com'
BACKTORY_MASTER_ACCESS_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjpudWxsLCJpc19ndWVzdCI6ZmFsc2UsInNjb3BlIjpbIm1hc3RlciJdLCJleHAiOjE1MTg1MzgzNzIsImp0aSI6Ijk5ZThkYzQ0LWU5YjktNDE1NS05NjViLWRiMzZhMWQyNTAxZCIsImNsaWVudF9pZCI6IjVhM2JhMmYwZTRiMDFhMjgxMTI4MjgwNyJ9.oHmTVHIVgIeLp8iwTTJNJjxrKAE4xHq42-_Tyv8f2S3azNs5gAX7uroI3ecgmCsTM5IGcozpAPDv4hGV7y8YAG5yEFyL9cHnPIeuIjDQrjc4zlM-ot8zFLHDI5ad2i9nxInfQKp0HZbULhfi87bBvO1LEkSGD-6AAGF3GxgCff4xiZBAu8xEGfjD94kWcPxenJ7Ej_CDv76jevOliyF9ipwTIMJ5EkF61_ml20bBKXO-_Jy-Jh93Y_YiSQ64iP9cISuC0g-HF7PEweMOYhaE5Q3bzxQP5xlh6EPCXpbPvqye13U4Filr3KCD9kWvkqp6dQ4BJxKvKfDXZ8LG8Z1Pfg'

BACKTORY_STORAGE_ID = '5a3ba343e4b01a2811282b85'
BACKTORY_STORAGE_SERVICE_PREFIX = 'http://storage.backtory.com'
BACKTORY_STORAGE_SERVE_PREFIX = 'http://storage.backtory.com/hamclassy'


def storage_request(http_method, url, **kwargs):
    storage_header = {
        'X-Backtory-Storage-Id': BACKTORY_STORAGE_ID,
        'Authorization': 'Bearer ' + BACKTORY_MASTER_ACCESS_TOKEN
    }
    if 'headers' in kwargs:
        kwargs['headers'].update(storage_header)
    else:
        kwargs['headers'] = storage_header

    try:
        response = requests.api.request(
            http_method,
            BACKTORY_STORAGE_SERVICE_PREFIX + url,
            **kwargs
        )
    except requests.exceptions.ConnectionError:
        print('-- ConnectionErrorException --')
        return None

    status_code = response.status_code
    if 200 <= status_code <= 299:
        return response

    try:
        print(response.json())
    except json.decoder.JSONDecodeError:
        print(status_code)


def image_optimizer(source_filepath, size='50x', out_type='resize', quality=90):
    """
    Image Optimizer
    :return: is_success, filepath
    """
    orig_filename, file_ext = splitext(basename(source_filepath))
    converted_filename = str(uuid4()) + file_ext
    convert_filepath = join(dirname(source_filepath), converted_filename)

    convert_options = ''
    if out_type == 'crop':
        convert_options = '-resize "{}^" -gravity center -crop "{}+0+0" -quality {}'.format(
            size, size, quality)
    elif out_type == 'resize':
        convert_options = '-resize {} -quality {}'.format(size, quality)
    elif out_type == 'force_resize':
        convert_options = '-resize {}! -quality {}'.format(size, quality)

    convert_cmd = u'convert "{input_file}" {output_option} "{output_file}"'.format(
        input_file=source_filepath,
        output_option=convert_options,
        output_file=convert_filepath
    )

    convert_process = subprocess.Popen(convert_cmd,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT,
                                       shell=True)
    convert_process_result = convert_process.communicate()
    if convert_process_result[0]:
        print('- Failed optimize')
        return False, source_filepath

    print('- Success optimize')
    return True, convert_filepath


def get_md5sum(directory_name):
    command = u'md5sum "{}"'.format(directory_name).encode('utf-8')
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               shell=True)
    raw_result = process.communicate()
    return raw_result[0].decode('utf8').split(' ')[0]


def get_filesize(filepath):
    command = u'wc -c <  "{}"'.format(filepath).encode('utf-8')
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               shell=True)
    raw_result = process.communicate()
    return int(raw_result[0].decode('utf-8'))


def get_meta_info(filename):
    cmd_get_meta = u'exiftool -j "{filename}"'.format(filename=filename).encode('utf-8')
    process = subprocess.Popen(cmd_get_meta,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               shell=True)
    raw_result = process.communicate()
    meta = json.loads(str(raw_result[0]))[0]

    pop_keys = ['SourceFile', 'FileName', 'Directory', 'FilePermissions',
                'FileModifyDate', 'FileAccessDate', 'FileInodeChangeDate',
                'ExifToolVersion', 'Directory', 'Error']
    for key in pop_keys:
        if key in meta.keys():
            meta.pop(key)

    return meta


def upload_file_to_backtory(file):
    file_found = False
    klass = None
    for story in Story.objects.all():
        for pic in story.pics.all():
            if pic == file:
                file_found = True
                klass = story.kelaas.id

    for kelaas_post in Kelaas_post.objects.all():
        for kelaas_file in kelaas_post.files.all():
            if kelaas_file == file:
                klass = kelaas_post.kelaas.id

    if klass is None:
        return

    # print('File Found: ', file_found)

    source_filepath = settings.MEDIA_ROOT.replace('/media', '') + file.data.url
    source_filepath = urllib.unquote(source_filepath).decode('utf8')

    is_optimized = False
    if file_found:
        is_optimized, source_filepath = image_optimizer(source_filepath)
    else:
        source_filepath = source_filepath

    multiple_files = []
    data = []

    multiple_files.append(
        ('fileItems[0].fileToUpload', open(source_filepath, 'rb'))
    )

    if is_optimized:
        backtory_file_path = 'production/class/{}'.format(klass)
    else:
        backtory_file_path = 'production/class/{}/{}'.format(klass, file.uuid)

    data.append(
        ('fileItems[0].path', backtory_file_path)
    )
    data.append(
        ('fileItems[0].replacing', 'true')
    )

    backtory_response = storage_request(
        'post', '/files',
        files=multiple_files,
        data=data
    )

    if backtory_response is None:
        print('- Failed Upload', file.id)

    print('- Success Upload', file.id)

    saved_files_urls = backtory_response.json()['savedFilesUrls']
    backtory_response_split = saved_files_urls[0].split("/")
    # print(backtory_response_split)

    if is_optimized:
        real_filename = backtory_response_split[3]
        link = "{}/class/{}/{}".format(
            BACKTORY_STORAGE_SERVE_PREFIX,
            klass,
            real_filename
        )
    else:
        file_uuid = backtory_response_split[3]
        real_filename = backtory_response_split[4]
        link = "{}/class/{}/{}/{}".format(
            BACKTORY_STORAGE_SERVE_PREFIX,
            klass,
            file_uuid,
            real_filename
        )

    file.link = link
    file.is_optimized = is_optimized
    file.md5sum = get_md5sum(source_filepath)
    file.filesize = get_filesize(source_filepath)
    file.meta = get_meta_info(source_filepath)
    file.klass = klass
    file.save()


class Command(BaseCommand):
    help = "Upload Files To Backtory"

    def upload_files(self):
        for file in File.objects.filter(link__isnull=False).all():
            upload_file_to_backtory(file)

        # file = File.objects.get(id=25)
        # upload_file_to_backtory(file)
        print('************* Complete ****************')

    def handle(self, *args, **options):
        self.upload_files()
