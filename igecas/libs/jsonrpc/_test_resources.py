# /usr/bin/env false
# -*- coding: UTF-8 -*-

"""
Test Resources are used by the test_broker module.
"""
import decimal
from . import defaults

# pylint:disable=missing-docstring, no-self-use, invalid-name, global-statement
# pylint:disable=too-many-public-methods, star-args, too-few-public-methods
# pylint:disable=unused-argument

CLIENT_ID = 0

def echo(*args, **kwargs):
    "Echo function, whatever you put it returns as a string."
    tmp = ""
    for arg in args:
        tmp += "%s " % arg
    for key, value in kwargs.items():
        tmp += "%s:%s " % (key, value)
    tmp = tmp[:-1]
    return tmp

def ping():
    "Ping server available"
    return "pong"

def notification():
    "A notification that does not return anything."
    # Well it returns none by default.
    pass

@defaults.include_data
def with_data(one_argument, data):
    return(one_argument, 'got_data')

class BoundMethod(object):
    def nil(self):
        return "nil"

def raise_an_error():
    raise ValueError("A Function that errors")

def returns_decimal():
    return decimal.Decimal(1.2)

def make_rpc(function, *args, **kwargs):
    if len(kwargs) > 0:
        params = dict()
        for index, value in enumerate(args):
            params[str(index)] = value
        for key, value in kwargs.items():
            params[key] = value
    else:
        params = args

    global CLIENT_ID
    CLIENT_ID += 1

    rpc = {"id":CLIENT_ID, "jsonrpc":defaults.JSON_RPC_VERSION}

    if isinstance(function, str):
        rpc["method"] = function
    else:
        rpc["method"] = function.__name__

    rpc["params"] = params
    return rpc

def make_rpc_json(function, *args, **kwargs):
    rpc = make_rpc(function, *args, **kwargs)
    return defaults.json.dumps(rpc)

def execute(broker, rpc):
    returned = broker.execute(rpc)["exits"]
    dumped = defaults.json.loads(returned)
    if isinstance(dumped, list):
        return dumped
    elif isinstance(dumped, dict):
        key = "result"
        if "error" in dumped:
            key = "error"
        return dumped[key]

def make_call(broker, function, *args, **kwargs):
    json_rpc = make_rpc_json(function, *args, **kwargs)
    return execute(broker, json_rpc)


class PseudoFileHandler(object):
    def __init__(self):
        self.written = list()

    def write(self, data):
        self.written.append(data)

    def flush(self):
        pass


def with_allow_denied():
    pass # pragma: no cover
