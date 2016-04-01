# /usr/bin/env false
# -*- coding: UTF-8 -*-

"""
Defaults defined here can be monkey patched to extend the behaviour.
For example if you would like to handle Decimal and DateTime objects
serialisation you would replace the json import here.
"""
# pylint: disable=unused-import
import json

JSON_RPC_VERSION = "2.0"

REQUEST_OBJECT = {"id":None,
                  "jsonrpc":JSON_RPC_VERSION,
                  "method":None,
                  "params":None}

DATA = {"input":str(),   # The incoming JSON-RPC string
        "begin":list(),  # This contains the starting call arguments
        "index":0,       # Current position of calls list
        "calls":list(),  # Contains a sequence of CALL's
        "batch":False,   # Set to True if it is a batch
        "error":None,    # Set if there is an error other then within a call
        "debug":False,   # When enabled adds tracebacks and prints debug lines
        "names":dict(),  # Contains the function names and reference
        "exits":None}    # What is actually returned

CALL = {"call":None,     # The specific call
        "method":None,   # This is the actual function to be executed
        "plargs":list(), # Positional list arguments to be fed to function
        "kwargs":dict(), # Keyword arguments to be fed to function
        "error":None,    # Set to the error struct if there has one occurred
        "return":None,   # What the function actually returns
        "rpc_id":None,   # The rpc_id of the function
        "notification":False,} # Whether it is a notification call.

INTERNAL_ERROR = {"code":-32603,
                  "message":"Internal error",
                  "data":"Internal JSON-RPC error."}

RESPONSE_OBJECT = {"jsonrpc":JSON_RPC_VERSION,
                   "id":None,
                   } # Add a "result" or "error" key value.

def include_data(function):
    """
    This decorator signals the handler to include the data dictionary to the
    arguments that call the function, data will be passed down as a keyword
    argument where the key is 'data'.
    """
    function.__data__ = True
    return function
