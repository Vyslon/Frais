from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView


urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name='accueil.html'), login_url='login'), name='accueil'),
    path('admin/', admin.site.urls),
    path('', include('ppefrais.urls')),
    path('', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

