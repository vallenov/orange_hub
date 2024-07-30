from django.urls import re_path
from apps.hub_screen.views import (
    HubScreenBrightness
)

urlpatterns = [
    re_path(r'^brightness', HubScreenBrightness.as_view())
]
