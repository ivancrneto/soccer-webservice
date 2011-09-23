from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
     (r'^futebol/', include('futebol.base.urls')),
     

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^soap/', include('futebol.service.urls')),
    (r'^rest/', include('futebol.service.urls')),
    (r'^soap-server/', include('futebol.soap_server.urls')),
)


#descomentar isso para o servidor do django
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^public/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.dirname(__file__),
            'files/')}),
        (r'^static-media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.dirname(__file__),
            'media/')}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.dirname(__file__),
            '/home/ivan/tv-digital/django-server/env/lib/python2.6/site-packages/django/contrib/admin/media')}),
    )
