from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.nomenclature.urls')),
    path('', include('app.document.urls')),
    path('', include('app.contactor.urls')),
    path('', include('app.core.urls')),
    path('', include('app.autocomplete.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
