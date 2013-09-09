from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'niko.views.dashboard', name='dashboard'),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)$',
        'niko.views.dashboard', name='dashboard_dated'),
    url(r'^vote$', 'niko.views.vote', name='vote'),
    url(r'^save/(?P<mood>\w+)$', 'niko.views.save', name='save'),
    # url(r'^niko_niko/', include('niko_niko.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
