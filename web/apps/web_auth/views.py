import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

logger = logging.getLogger(__name__)


class LoginView(APIView):
    def post(self, request):
        return Response()


class LogoutView(APIView):
    def post(self, request):
        return HttpResponse()
