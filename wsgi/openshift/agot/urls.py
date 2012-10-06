from django.conf.urls.defaults import patterns, include, url
from resources import *
from views import *
from djangorestframework.views import ListOrCreateModelView, InstanceModelView


urlpatterns = patterns('',

    # customed view/handler
#    (r'poll/(?P<pid>[^/]+)/choice/(?P<cid>[^/]+)', RESTforPollAndChoice.as_view(resource=ChoiceItemResource)),
#    (r'poll/', RESTforPoll.as_view(resource=PollItemResource)),
                       
    # built-in view/handler
    (r'cycle/(?P<id>[^/]+)', InstanceModelView.as_view(resource=CycleItemResource)),
    (r'cycle/', ListOrCreateModelView.as_view(resource=CycleItemResource)),
    (r'package/(?P<id>[^/]+)', InstanceModelView.as_view(resource=PackageItemResource)),
    (r'package/', ListOrCreateModelView.as_view(resource=PackageItemResource)),
    (r'card/(?P<id>[^/]+)', InstanceModelView.as_view(resource=CardItemResource)),
    (r'card/', ListOrCreateModelView.as_view(resource=CardItemResource)),
)
