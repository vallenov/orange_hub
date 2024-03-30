from django.urls import re_path
from apps.light.views import (
    MainLEDPower,
    MainLEDColor,
    MainLEDBrightness,
    MainLEDEffect,
    MainLEDEffectSpeed,
)

urlpatterns = [
    re_path(r'^main_led/power', MainLEDPower.as_view()),
    re_path(r'^main_led/color', MainLEDColor.as_view()),
    re_path(r'^main_led/brightness', MainLEDBrightness.as_view()),
    re_path(r'^main_led/effect', MainLEDEffect.as_view()),
    re_path(r'^main_led/effect_speed', MainLEDEffectSpeed.as_view())
]
