from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required
from main.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'coding_experiments.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$', 'main.views.home', name='home'),
    url(r'^landing/(?P<cnd>\d+)/$', 'main.views.landing', name='landing'),
    url(r'^landing/$', 'main.views.landing', name='landing'),
    url(r'^instructions/$', 'main.views.instructions', name='instructions'),
    url(r'^instructions/(?P<page>\d+)/$', 'main.views.instructions', name='instructions'),
    url(r'^coding/((?P<page>\d+)/|)$', 'main.views.coding', name='coding'),
    url(r'^thanks/$', 'main.views.thanks', name='thanks'),
    url(r'^validate/((?P<page>\d+)/|)$', 'main.views.validate', name='validate'),
    url(r'^survey/pre/$', 'main.views.pre_survey', name='pre_survey'),
    url(r'^survey/post/$', 'main.views.post_survey', name='post_survey'),
    url(r'^reqcheck/$', 'main.views.req_check', name='req_check'),
    url(r'^instructioncheck/$', InstructionCheck.as_view(), name='instruction_check'),
    url(r'^pause/$', 'main.views.bonus_check', name='bonus_check'),

    url(r'^$', HomeView.as_view(), name='user_home'),
    url(r'^coding2/(?P<assignment_id>\d+)/$', UserCodingView.as_view(), name='user_coding'),


    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),    
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
