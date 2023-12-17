from django.urls import path, include

from malinka_web.malinka_web.apps.views import MainPage

urlpatterns = [
    path('', MainPage.as_view()),
    #path('admin/', include('admin.urls')),
    path('auth/', include('web_auth.urls')),
]
