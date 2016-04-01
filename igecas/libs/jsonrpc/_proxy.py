# /usr/bin/env false
# _*_ coding: UTF_8 _*_

"""
Proxy Client
"""

import requests
from requests.packages.urllib3 import exceptions
from . import defaults

def _make_params(plargs, kwargs):
    "Convert arguments into params"
    # In JSON-RPC you can only do a struct or list for param.
    # Considering python has both, but does not allow the key of a keyword
    # argument to be an integer, we use that fact to combine list arguments
    # and keyword arguments by making the key an integer.

    if len(kwargs) == 0:
        # If we have no keyword arguments don't bother with anything.
        return plargs

    params = dict()

    for index, arg in enumerate(plargs):
        params[str(index)] = arg

    for key, value in kwargs.items():
        params[key] = value

    return params

def _make_url(host='localhost', port='80', use_tls=False, path='api'):
    "Make the url"
    url = "http"
    if use_tls:
        url += "s"
    url += "://"
    url += host
    if str(port) != "80":
        url += ":"
        url += str(port)
    url += "/"

    while path.startswith('/'):
        path = path[1:]

    while path.endswith('/'):
        path = path[:-1]

    url += path
    url += '/'
    return url


class JSONRPCERROR(ValueError):               # pylint:disable=missing-docstring
    pass


class RPC(object):
    "Wrapper for the RPC function"
    CLASS_NAME = "%s (JSON-RPC Proxy call to %s)"
    def __init__(self, proxy, name):
        self.proxy = proxy
        self.name = name
        self.is_notification = False

    # Normally I would no bother with toggeling bools, but in this case I
    # wanted to add two functions to keep pylint happy and it provides some
    # implicit documentation.
    def set_notification(self):
        "Indicate this call is a notification."
        self.is_notification = True

    def set_expect_return_data(self):
        "Indicate that we want the output of the function returned."
        self.is_notification = False

    def __getattr__(self, name):
        name = self.name + '.' + name
        text = self.CLASS_NAME % (name, self.proxy.__url__)
        rpc_class = type(text, (self.__class__,), {})
        instance = rpc_class(self.proxy, name)
        return instance

    def __call__(self, *args, **kwargs):
        rpc = defaults.REQUEST_OBJECT.copy()
        if self.is_notification:
            rpc.pop("id")
        else:
            rpc["id"] = self.proxy.__rpcid__
            self.proxy.__rpcid__ += 1

        rpc["method"] = self.name
        params = _make_params(args, kwargs)
        if len(params) > 0:
            rpc["params"] = params
        else:
            rpc.pop("params")

        try:
            json_rpc = defaults.json.dumps(rpc)
            request = self.proxy.__session__.post(self.proxy.__url__,
                                                  data=json_rpc)
            response = request.content.decode('utf-8')
            if len(response.strip()) == 0:
                response = {'result':None}
            else:
                response = defaults.json.loads(response)
        except exceptions.HTTPError as exception_instance:
            # We simulate an rpc error so we can handle it all the same.
            response = defaults.RESPONSE_OBJECT.copy()
            response["id"] = rpc["id"]
            error = {"code":-32700,
                     "message":exception_instance.__class__.__name__}
            tmp = list()
            for arg in exception_instance.args:
                tmp.append(str(arg))

            tmp.append("URL='%s'" % self.proxy.__url__)
            error["data"] = " ".join(tmp)
            response["error"] = error

        except UnicodeDecodeError:
            response = defaults.RESPONSE_OBJECT.copy()
            response["id"] = rpc["id"]
            response["error"] = {"code":-32700,
                                 "message":"Encoding Error",
                                 "data":"Server response is not in UTF-8."}
            
        except ValueError:
            response = defaults.RESPONSE_OBJECT.copy()
            response["id"] = rpc["id"]
            response["error"] = {"code":-32700,
                                 "message":"Value Error",
                                 "data":request.content.decode('utf-8')}


        if "error" in response:
            text = "%s(%s)" % (response["error"]["message"],
                                 response["error"]["code"])
            # pylint: disable=invalid-name
            ErrorClass = type(text, (JSONRPCERROR,), {})
            raise ErrorClass(response["error"]["data"])

        return response["result"]


class BaseProxy(object):                 #pylint: disable=too-few-public-methods
    """
    This clients proxies a request to a JSON-RPC enabled server.
    Instantiate this class and then call the remote function like it is a local
    one, for example if the remote function is 'echo' is on the server
    example.com and the api is exposed on the path api you would do this:
    rpc = Proxy(host='example.com', path='api)
    rpc.echo('arguments to the function')
    """
    def __init__(self, host='localhost', port='80', use_tls=False, path='api'):
        """
        Set proxy variable as internal ones so they don't clash with whatever
        the remote function names are.
        """
        self.__url__ = _make_url(host, port, use_tls, path)
        self.__rpcid__ = 0
        self.__session__ = requests.Session()
        self.__session__.headers["Content-Type"] = "application/json-rpc"
        self.__session__.headers["Accept"] = "application/json-rpc"

    def __getattr__(self, name):
        text = RPC.CLASS_NAME % (name, self.__url__)
        rpc_class = type(text, (RPC,), {})
        instance = rpc_class(self, name)
        return instance
