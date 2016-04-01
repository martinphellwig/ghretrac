from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^inacar/', include('inacar.urls')),
    url(r'^igecas/', include('igecas.urls')),
    url(r'^dosteps/', include('dosteps.urls')),
)
