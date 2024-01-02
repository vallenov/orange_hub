from django.urls import path, include

from apps.views import MainPage

urlpatterns = [
    path('', MainPage.as_view()),
    #path('admin/', include('admin.urls')),
    path('auth/', include('web_auth.urls')),
]
