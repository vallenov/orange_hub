from django.urls import re_path

from malinka_web.malinka_web.apps.malinka_auth.views import (
    LoginView,
    LogoutView
)

urlpatterns = [
    re_path(r'^login$', LoginView.as_view()),
    re_path(r'^logout$', LogoutView.as_view()),
]

