"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import handler403, handler404

from config import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

handler403 = 'vcars.views.custom_403'
handler404 = 'vcars.views.custom_404'
handler500 = 'vcars.views.custom_500'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vcars.urls', namespace='vcars')),
    path('api/', include('vcars_api.urls', namespace='api_vcars')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('chat/', include('chat.urls')),
    path('', include('game.urls', namespace='game')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
