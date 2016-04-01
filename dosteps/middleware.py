import threading
from .models import Workflow
from django.db import connection

class RequestThreadingLocal(object):
    """
    """
    threading_local = threading.local()
    threading_local.request = None

    def process_request(self, request):
        "Make the request thread local available."
        self.threading_local.request = request
        
        