from django.conf.urls.defaults import *
import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^tools/', include('tools.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^user/', include('tools.tiq_login.urls')),
    (r'^tags/', include('tools.tags.urls')),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
    	{'document_root':  settings.STATIC_DOC_ROOT}),
    (r'', 'dashboard.views.index')
)
