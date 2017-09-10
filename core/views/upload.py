import json

from django.http import HttpResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser


@api_view(['POST'])
@parser_classes((MultiPartParser, FormParser))
def upload_file(request):
    if not request.user.is_authenticated:
        return HttpResponse('user not authenticated', status=401)

    if 'data' in request.FILES:
        uploaded_file = request.FILES['data']

        f = File(
            title=request.POST.get('title', uploaded_file.name),
            description=request.POST.get('description', 'بدون توضیح'),
            data=uploaded_file
        )
        f.owner = request.user.person
        f.save()

        return HttpResponse(json.dumps({
            'id': f.id,
            'url': f.url,
            'title': f.title
        }), status=202)
    return HttpResponse('bad data input', status=400)