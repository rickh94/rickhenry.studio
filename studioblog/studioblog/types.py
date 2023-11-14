from types import FunctionType

from django.http import HttpRequest
from django.views import generic
from django_htmx.middleware import HtmxDetails
from wagtail.models import models


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


class HtmxView(generic.View):
    request: HtmxHttpRequest


class WagtailPageManager(models.Manager):
    live: FunctionType
