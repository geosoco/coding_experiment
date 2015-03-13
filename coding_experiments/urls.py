from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from rest_framework import routers


urlpatterns = patterns('',
    # Examples:
    url(r'^', include('main.urls')),
    url(r'^api/', include('api.urls')),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
) #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

"""
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
"""