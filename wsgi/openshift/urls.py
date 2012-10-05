from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import poll.urls
import agot.urls

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'openshift.views.home', name='home'),
    url(r'^about/', 'openshift.views.about', name='about'),

    
    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
                       
    # Urls of installed app
    (r'^poll/', include(poll.urls.urlpatterns)),
    (r'^agot/', include(agot.urls.urlpatterns)),
)

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT )
                     
