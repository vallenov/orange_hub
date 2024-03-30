import logging

from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render

from apps.utils.esp8266.esp import esp

logger = logging.getLogger(__name__)


class MainLEDPower(APIView):

    def get(self, request):
        esp.main_led.power_switch()
        context = {
            'power': True if esp.main_led.power else False
        }
        return render(request, template_name='main.html', context=context)


class MainLEDColor(APIView):

    def get(self, request):
        val = request.GET.get('id')
        if val:
            esp.main_led.color_switch(val=val)
        return HttpResponse(status=200)


class MainLEDBrightness(APIView):

    def get(self, request):
        val = request.GET.get('id')
        if val:
            esp.main_led.brightness_switch(val=val)
        return HttpResponse(status=200)


class MainLEDEffect(APIView):

    def get(self, request):
        val = request.GET.get('id')
        if val:
            esp.main_led.effect_switch(val=val)
        return HttpResponse(status=200)


class MainLEDEffectSpeed(APIView):

    def get(self, request):
        val = request.GET.get('id')
        if val:
            esp.main_led.effect_speed_switch(val=val)
        return HttpResponse(status=200)
