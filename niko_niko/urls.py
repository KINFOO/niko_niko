from django.conf.urls import patterns, include, url

# Enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'niko.views.polls', name='polls'),
    url(r'^polls/$', 'niko.views.polls'),
    url(r'^polls/(?P<slug>\w+)/$', 'niko.views.poll', name='poll'),
    url(r'^polls/(?P<slug>\w+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)$',
        'niko.views.poll', name='poll_dated'),
    url(r'^polls/(?P<slug>\w+)/vote$', 'niko.views.vote', name='vote'),
    url(r'^polls/(?P<slug>\w+)/save/(?P<mood>\w+)$', 'niko.views.save', name='save'),
    # url(r'^niko_niko/', include('niko_niko.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
