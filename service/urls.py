from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('futebol.service.views.soap',
    (r'^$', 'bla'),
)

#urlpatterns += patterns('futebol.service.views.rest',
#    (r'^$', 'bla'),
#)




