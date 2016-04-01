from django.conf import settings
from django.conf.urls import patterns, url
from . import views
from .libs import jsonrpc
from . import api

class Broker(jsonrpc.DjangoBroker):
    "DjangoBroker class implementing allow."
    def allow(self, data):
        request = data["begin"]
        if request.user.is_authenticated():
            self.print('#' * 80)
            self.print(request.user)
            self.print('#' * 80)
            return True
        return False

_BROKER = Broker(debug=True)

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url('api', _BROKER, name='api'),
)

for item in dir(api):
    if not item.startswith('_'):
        subject = getattr(api, item)
        _BROKER.add(subject)

