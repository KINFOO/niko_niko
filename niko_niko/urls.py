from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

# Enable the admin:
from django.contrib import admin
admin.autodiscover()

handler404 = 'niko.views.handler404'

urlpatterns = patterns('',
    url(r'^$', 'niko.views.polls', name='polls'),
    url(r'^polls/$', 'niko.views.polls'),
    url(r'^polls/(?P<slug>[\w-]+)/$', 'niko.views.poll', name='poll'),
    url(r'^polls/(?P<slug>[\w-]+)/vote/$', 'niko.views.vote', name='vote'),
    url(r'^polls/(?P<slug>[\w-]+)/qrcode/$', 'niko.views.qr_code_page', name='qrcode'),
    url(r'^polls/(?P<slug>[\w-]+)/svg/$', 'niko.views.qr_code_image', name='svg'),
    url(r'^polls/(?P<slug>[\w-]+)/save/(?P<mood>\d{1})$', 'niko.views.save', name='save'),
    # url(r'^niko_niko/', include('niko_niko.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # Serving admin static files
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
