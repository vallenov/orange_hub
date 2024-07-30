import logging

from rest_framework.views import APIView
from django.http import HttpResponse

from apps.utils.esp8266.esp import esp

logger = logging.getLogger(__name__)


class HubScreenBrightness(APIView):

    def get(self, request):
        val = request.GET.get('id')
        if val:
            esp.screen.brightness_switch(val=val)
        return HttpResponse(status=200)
