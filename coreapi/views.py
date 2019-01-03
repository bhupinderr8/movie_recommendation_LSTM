from django.http import HttpResponse
from . import helper


def index(request):
    json_response = helper.generate_list(request.body)
    return HttpResponse(json_response)

