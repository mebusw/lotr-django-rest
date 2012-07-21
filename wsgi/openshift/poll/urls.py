from django.conf.urls.defaults import patterns, include, url
from poll.resources import *
from poll.views import *
from djangorestframework.views import ListOrCreateModelView, InstanceModelView



urlpatterns = patterns('',
    # customed view/handler
    (r'poll/(?P<pid>[^/]+)/choice/(?P<cid>[^/]+)', RESTforAPoll.as_view(resource=PollItemResource)),
                       
    # built-in view/handler
    (r'choice/(?P<id>[^/]+)', InstanceModelView.as_view(resource=ChoiceItemResource)),
    (r'choice/', ListOrCreateModelView.as_view(resource=ChoiceItemResource)),
    (r'cycle/(?P<id>[^/]+)', InstanceModelView.as_view(resource=CycleItemResource)),
    (r'cycle/', ListOrCreateModelView.as_view(resource=CycleItemResource)),
    (r'package/(?P<id>[^/]+)', InstanceModelView.as_view(resource=PackageItemResource)),
    (r'package/', ListOrCreateModelView.as_view(resource=PackageItemResource)),
    (r'poll/', ListOrCreateModelView.as_view(resource=PollItemResource)),
                       

)

