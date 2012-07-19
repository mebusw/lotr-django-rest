from django.conf.urls.defaults import patterns, include, url
from poll.resources import *
from poll.views import *
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
    
    # built-in view/handler
    url(r'^api/choice/(?P<id>[^/]+)', InstanceModelView.as_view(resource=ChoiceItemResource)),
    url(r'^api/choice/', ListOrCreateModelView.as_view(resource=ChoiceItemResource)),
                       
    # customed view/handler
    url(r'^api/poll/(?P<id>[^/]+)', RESTforAPoll.as_view(resource=PollItemResource)),
    url(r'^api/poll/', ListOrCreateModelView.as_view(resource=PollItemResource)),
)

