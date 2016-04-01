# /usr/bin/env false
# -*- coding: UTF-8 -*-

"""
This module implements the processes that do the actually processing of the rpc,
note that most processes assume that the input is a data structure as defined in
defaults.DATA.
"""
import inspect
from . import defaults
from . import _base
# pylint: disable=broad-except, no-self-use, star-args

class ParseJSON(_base.Process):
    "Try parsing the json string or return an error."
    ERROR_CODE = -32700
    ERROR_MESSAGE = "Parse error"
    EXCEPTIONS = (ValueError, TypeError)
    SKIP_ON_ERROR = False

    def on_error_data(self, call, exception_instance):
        returns = "Parsing JSON string '%s' failed." % call
        return returns

    def process(self, data):
        data["input"] = defaults.json.loads(data["input"])


class MakeBatch(_base.Process):
    "Try making a batch out of it."
    ERROR_CODE = -32600
    ERROR_MESSAGE = "Invalid Request"
    EXCEPTIONS = (ValueError, )
    SKIP_ON_ERROR = True

    def on_error_data(self, call, exception_instance):
        returns = "Failed processing RPC '%s', it is not a call or batch."
        returns = returns % call
        return returns

    def process(self, data):
        value = data["input"]
        data["calls"] = list()

        if isinstance(value, (list, tuple)):
            data["batch"] = True
        elif isinstance(value, dict):
            data["batch"] = False
            value = [value,]
        else:
            raise ValueError("Invalid input '%s'" % value)

        for item in value:
            appendee = defaults.CALL.copy()
            appendee["call"] = item
            data["calls"].append(appendee)


class VerifyRPC(_base.Process):
    "Verify whether the RPC is valid according to JSON-RPC 2.0"
    ERROR_CODE = -32600
    ERROR_MESSAGE = "Invalid Request"
    EXCEPTIONS = (ValueError, )
    SKIP_ON_ERROR = True
    ITERATE_OVER_CALLS = True

    def on_error_data(self, call, exception_instance):
        returns = exception_instance.args[0]
        return returns

    def _assess_keys(self, rpc):
        "Check if there are keys that are not valid."
        invalid_arguments = list()
        call = rpc["call"]
        tmp = dict()

        for key in call:
            test = key.strip().lower()
            if test not in defaults.REQUEST_OBJECT.keys():
                invalid_arguments.append(key)
            tmp[test] = call[key]

        if len(invalid_arguments) > 0:
            text = ("Call '%s' has the following invalid arguments %s, "
                    "allowed keys are %s" )
            text = text % (call, invalid_arguments,
                           defaults.REQUEST_OBJECT.keys())
            raise ValueError(text)
        else:
            rpc["call"] = tmp

    def _assess_version(self, rpc):
        "Assess the correct version."
        text = None

        if "jsonrpc" not in rpc["call"]:
            text = "JSON-RPC parameter 'version' is required in call %s."
            text = text % rpc["call"]
        else:
            if rpc["call"]["jsonrpc"] != defaults.JSON_RPC_VERSION:
                text = ("JSON-RPC version '%s' not supported in call %s, "
                        "required '%s'") % (rpc["call"]["jsonrpc"], rpc["call"],
                                            defaults.JSON_RPC_VERSION)
        if text != None:
            raise ValueError(text)

    def _assess_method(self, rpc):
        "Assess if we have the key 'method'."
        if "method" not in rpc["call"]:
            text = "JSON-RPC parameter 'method' is required in call %s."
            text = text % rpc["call"]
            raise ValueError(text)

    def _assess_id(self, rpc):
        "Assess the id"
        if "id" in rpc["call"] and rpc["call"]["id"] != None:
            rpc["rpc_id"] = rpc["call"]["id"]
        else:
            rpc["notification"] = True

    def process(self, data):
        rpc =  data["calls"][data["index"]]

        self._assess_keys(rpc)
        self._assess_version(rpc)
        self._assess_method(rpc)
        self._assess_id(rpc)


class FindMethod(_base.Process):
    "Verify whether the RPC is valid according to JSON-RPC 2.0"
    ERROR_CODE = -32601
    ERROR_MESSAGE = "Method not found"
    EXCEPTIONS = (KeyError, )
    SKIP_ON_ERROR = True
    ITERATE_OVER_CALLS = True

    def on_error_data(self, call, exception_instance):
        returns = "The method '%s' does not exist / is not available."
        returns = returns % call["method"]
        return returns

    def process(self, data):
        rpc =  data["calls"][data["index"]]
        method = rpc["call"]["method"]
        rpc["function"] = data["names"][method]["function"]


class VerifyAccess(_base.Process):
    "Verify whether the RPC is valid according to JSON-RPC 2.0"
    ERROR_CODE = -32604
    ERROR_MESSAGE = "Access Denied"
    EXCEPTIONS = (ValueError, )
    SKIP_ON_ERROR = True
    ITERATE_OVER_CALLS = True

    def on_error_data(self, call, exception_instance):
        text = "Execution of method '%s' is prohibited under current context."
        text = text % call["method"]
        return text

    def process(self, data):
        call =  data["calls"][data["index"]]
        function = call["call"]["method"]
        do_check = data["names"][function]["do_check"]
        if do_check:
            if not data["allow"](data):
                raise ValueError('Access denied')


class VerifyParameters(_base.Process):
    "Verify whether the RPC is valid according to JSON-RPC 2.0"
    ERROR_CODE = -32602
    ERROR_MESSAGE = "Invalid params"
    EXCEPTIONS = (TypeError, )
    SKIP_ON_ERROR = True
    ITERATE_OVER_CALLS = True

    def on_error_data(self, call, exception_instance):
        returns = "Invalid method parameter(s); %s."
        returns = returns % exception_instance.args[0]
        return returns

    def process(self, data):
        plargs = list()
        kwargs = dict()
        rpc =  data["calls"][data["index"]]

        if "params" in rpc["call"] and rpc["call"]["params"] != None:
            params = rpc["call"]["params"]
            if isinstance(params, (list, tuple)):
                plargs = list(params)
            elif isinstance(params, dict):
                tmp = list()
                for key, value in params.items():
                    if key.isdigit():
                        tmp.append([key, value])
                    else:
                        kwargs[key] = value
                tmp.sort()
                for pair in tmp:
                    plargs.append(pair[1])
            else:
                plargs.append(params)

        if hasattr(rpc["function"], '__data__'):
            kwargs['data'] = data

        inspect.getcallargs(rpc["function"], *plargs, **kwargs)

        rpc["plargs"] = plargs
        rpc["kwargs"] = kwargs


class ExecuteCall(_base.Process):
    "The actual execution of the RPC."
    ERROR_CODE = -32603
    ERROR_MESSAGE = "Internal error"
    EXCEPTIONS = (Exception, )
    SKIP_ON_ERROR = True
    ITERATE_OVER_CALLS = True

    def on_error_data(self, call, exception_instance):
        returns = "Internal JSON-RPC error.; %s."
        returns = returns % exception_instance.args[0]
        return returns

    def process(self, data):
        rpc =  data["calls"][data["index"]]
        function = rpc["function"]
        plargs = rpc["plargs"]
        kwargs = rpc["kwargs"]
        rpc["return"] = function(*plargs, **kwargs)


class VerifyOutputCompatibleToJSON(_base.Process):
    "The actual execution of the RPC."
    ERROR_CODE = -32603
    ERROR_MESSAGE = "Internal error"
    EXCEPTIONS = (TypeError, )
    SKIP_ON_ERROR = True
    ITERATE_OVER_CALLS = True

    def on_error_data(self, call, exception_instance):
        returns = "Internal JSON-RPC error.; Output of function '%s': %s ."
        returns = returns % (call["method"], exception_instance.args[0])
        return returns

    def process(self, data):
        output = data["calls"][data["index"]]["return"]
        defaults.json.dumps(output)


class BuildResponse(_base.PostProcess):
    "Build the response, if there was an error, we need to wrap it."
    def process(self, data):
        "This is the entry process."
        returns = list()
        for call in data["calls"]:
            if call["notification"]:
                continue

            response = defaults.RESPONSE_OBJECT.copy()
            response["id"] = call["rpc_id"]
            if call["error"] != None:
                response["error"] = call["error"]
            else:
                response["result"] = call["return"]

            returns.append(response)

        if not data["batch"]:
            if len(returns) > 0:
                returns = returns[0]
            else:
                returns = None
        else:
            if len(returns) == 0:
                returns = None

        if data["error"] != None:
            # High level error that occurred before we can see the id
            returns = defaults.RESPONSE_OBJECT.copy()
            returns["error"] = data["error"]

        data["exits"] = returns


class DumpToJson(_base.PostProcess):
    "Dump to JSON"
    # If json dump despite being tested still complains, it will be handled,
    # this will most likely happen if a faulty extension is made, thus in the
    # vanilla system this is _very_ unlikely to occur.
    def process(self, data):
        try:
            response = defaults.json.dumps(data["exits"])
        except TypeError as exception_instance:
            error = defaults.INTERNAL_ERROR.copy()
            error["data"] += '\n' + str(exception_instance)
            response = defaults.RESPONSE_OBJECT.copy()
            response["error"] = error
            response = defaults.json.dumps(response)

        data["exits"] = response
