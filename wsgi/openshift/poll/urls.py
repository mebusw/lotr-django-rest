from django.conf.urls.defaults import patterns, include, url
from poll.resources import *
from poll import views
from poll.views import *
from djangorestframework.views import ListOrCreateModelView, InstanceModelView


urlpatterns = patterns('',

    # customed view/handler
    (r'poll/(?P<pid>[^/]+)/choice/(?P<cid>[^/]+)', RESTforPollAndChoice.as_view(resource=PollItemResource)),
    (r'poll/', RESTforPoll.as_view(resource=PollItemResource)),
                       
    # built-in view/handler
    (r'choice/(?P<id>[^/]+)', InstanceModelView.as_view(resource=ChoiceItemResource)),
    (r'choice/', ListOrCreateModelView.as_view(resource=ChoiceItemResource)),
    (r'cycle/(?P<id>[^/]+)', InstanceModelView.as_view(resource=CycleItemResource)),
    (r'cycle/', ListOrCreateModelView.as_view(resource=CycleItemResource)),
    (r'package/(?P<id>[^/]+)', InstanceModelView.as_view(resource=PackageItemResource)),
    (r'package/', ListOrCreateModelView.as_view(resource=PackageItemResource)),
)

# urlpatterns += patterns('openshift.poll.views',
   # url(r'tolls/', 'index'),
# )

urlpatterns += patterns('',
    url(r'tolls/', index),
)