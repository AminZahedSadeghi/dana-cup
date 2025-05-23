from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include

from .api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('sonar/', include('django_sonar.urls')),
    re_path(r'^rosetta/', include('rosetta.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
