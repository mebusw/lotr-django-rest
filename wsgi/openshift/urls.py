from django.conf.urls.defaults import patterns, include, url
#from poll.models import Poll, Choice
from poll.resources import *
from djangorestframework.views import ListOrCreateModelView, InstanceModelView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'openshift.views.home', name='home'),
    # url(r'^openshift/', include('openshift.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    #########
    url(r'^about/', 'openshift.views.about', name='about'),
    
    url(r'^polls/$', 'openshift.poll.views.index'),
    url(r'^polls/(?P<poll_id>\d+)/$', 'openshift.poll.views.detail'),
    url(r'^polls/(?P<poll_id>\d+)/results/$', 'openshift.poll.views.results'),
    url(r'^polls/(?P<poll_id>\d+)/vote/$', 'openshift.poll.views.vote'),   
    url(r'^api/choice/', ListOrCreateModelView.as_view(resource=LineItemResource)),
)
