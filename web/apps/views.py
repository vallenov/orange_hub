import logging

from rest_framework.views import APIView
from django.shortcuts import render

logger = logging.getLogger(__name__)


class MainPage(APIView):

    def get(self, request):
        return render(request, template_name='main.html')
