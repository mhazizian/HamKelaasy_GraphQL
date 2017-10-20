import json

from django.http import HttpResponse

from core.errors_code import errors


def error_doc(request):
    return HttpResponse(
        '<html><body><pre><code>'
        + json.dumps(errors, indent=4, sort_keys=True)
        + '</code></pre></body></html>'
    )


def notification_doc(request):
    pass
