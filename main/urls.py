from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from main.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'coding_experiments.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'main.views.home', name='home'),
    url(r'^landing/$', 'main.views.landing', name='landing'),
    url(r'^instructions/$', 'main.views.instructions', name='instructions'),
    url(r'^instructions/(?P<page>\d+)/$', 'main.views.instructions', name='instructions'),
    url(r'^coding/((?P<page>\d+)/|)$', 'main.views.coding', name='coding'),
    url(r'^thanks/$', 'main.views.thanks', name='thanks'),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
