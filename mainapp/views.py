from django.http import HttpResponse
from django.views.generic import TemplateView


def hello_view(request):
    return HttpResponse("Hello world")
