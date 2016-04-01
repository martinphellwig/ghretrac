# /usr/bin/env false
# -*- coding: UTF-8 -*-

"""
These are Django specific Broker and Client, the biggest difference is that
these include an authentication mechanism.
"""
import sys
from ._broker import BaseBroker
from ._proxy import BaseProxy
from ._proxy import RPC as BaseRPC
from ._proxy import JSONRPCERROR

from . import defaults

################################################################################
# Django Broker
################################################################################
try:
    from django.http import HttpResponse as DjangoHttpResponse
except ImportError:                                           # pragma: no cover
    # pylint:disable=invalid-name
    DjangoHttpResponse = None

@defaults.include_data
def _django_login(identifier, passphrase, data):
    "Log a user in via the API."
    from django.contrib.auth import authenticate
    from django.contrib.auth import login as _login
    user = authenticate(username=identifier, password=passphrase)
    if user is not None:
        request = data["begin"]
        _login(request, user)
        return True
    return False

@defaults.include_data
def _django_logout(data):
    "log the user out"
    from django.contrib.auth import logout as _logout
    _logout(data["begin"])
    return True

def _django_ping():
    "Ping server available"
    return "pong"


class Broker(BaseBroker):
    """
    Django Broker
    """
    def __init__(self, debug=False, out=sys.stderr):
        if DjangoHttpResponse == None:                        # pragma: no cover
            text = "Can not import 'HttpResponse' from 'django.http'."
            raise ImportError(text)

        check_allow=True
        BaseBroker.__init__(self, check_allow, debug, out)
        self.csrf_exempt = True
        self.add(_django_login, 'django.login', check_allow=False)
        self.add(_django_logout, 'django.logout')
        self.add(_django_ping, 'django.ping')

    def allow(self, data):
        request = data["begin"]
        return request.user.is_authenticated()

    def __call__(self, request):
        "The request handler"
        content = ""
        content_type = ""
        status = 200

        if not request.method == 'POST':
            content = "ERROR 400 BAD REQUEST: JSON-RPC over POST only."
            status = 400
        else:
            try:
                json_rpc = request.body.decode('utf-8')
                data = self.execute(json_rpc, request)
                if not data['batch']:
                    if len(data['calls']) > 0 \
                                           and data['calls'][0]['notification']:
                        status = 204
                        content = None

                if status == 200:
                    content = data["exits"]

            except UnicodeDecodeError:
                response = defaults.RESPONSE_OBJECT.copy()
                response["error"] = {"code":-32700,
                                     "message":"Encoding Error",
                                     "data":"JSON-RPC is UTF-8 only."}
                content = defaults.json.dumps(response)

        return DjangoHttpResponse(content=content,
                                  content_type=content_type,
                                  status=status)


################################################################################
# Django Proxy
################################################################################
class RPC(BaseRPC):
    "Override the RPC mechanism as with our django client we expect to login."
    def __call__(self, *args, **kwargs):
        try:
            returns = BaseRPC.__call__(self, *args, **kwargs)
            return returns
        except JSONRPCERROR as exception_instance:
            test = exception_instance.args[0].lower()
            if 'prohibited' in test:
                self.proxy.__login__()
                returns = BaseRPC.__call__(self, *args, **kwargs)
                return returns

            # Will only occur in circumstances that can't be tested reasonably.
            raise exception_instance                          # pragma: no cover


class Proxy(BaseProxy):                  #pylint: disable=too-few-public-methods
    """
    Make Proxy resilient against session timeouts by catching the error and
    logging in again."""
    # pylint: disable=too-many-arguments
    def __init__(self, identifier=None, passphrase=None,
                        host='localhost', port='80', use_tls=False, path='api'):
        BaseProxy.__init__(self, host, port, use_tls, path)
        self.__identifier__ = identifier
        self.__passphrase__ = passphrase
        self.__login__()

    def __login__(self):
        if self.__identifier__ == None and self.__passphrase__ == None:
            pass
        else:
            try:
                result = self.django.login(self.__identifier__,
                                           self.__passphrase__)
            except JSONRPCERROR as exception_instance:
                if 'connection refused' in exception_instance.args[0].lower():
                    print('!!! Warning !!! %s' % exception_instance.args[0],
                          file=sys.stderr)
                result = None

            if result == False:
                text = "Identifier/Passphrase combination does not match."
                raise JSONRPCERROR(text)

    def __getattr__(self, name):
        text = RPC.CLASS_NAME % (name, self.__url__)
        rpc_class = type(text, (RPC,), {})
        instance = rpc_class(self, name)
        return instance

