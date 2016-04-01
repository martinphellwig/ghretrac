# /usr/bin/env false
# _*_ coding: UTF_8 _*_

"""
testing module
"""
# pylint:disable=missing-docstring, no-self-use, invalid-name
# pylint:disable=too-many-public-methods, star-args

import unittest
from . import defaults
from . import _broker
from . import _processes
from . import _test_resources as tr
# helper functions
from ._test_resources import\
    make_rpc, execute, PseudoFileHandler
# test functions
from ._test_resources import\
    echo, ping, notification, raise_an_error, returns_decimal, with_data, \
    with_allow_denied

class TestWorks(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.maxDiff = None
        self.rpc = _broker.BaseBroker(debug=False)
        self._method = tr.BoundMethod().nil
        for function in [self._method, echo, ping, notification, raise_an_error,
                         returns_decimal, with_data]:
            self.rpc.add(function, check_allow=False)
        self.rpc.add(with_allow_denied)

    def test_001_method_nil(self):
        function = self._method
        expected = function()
        returned = tr.make_call(self.rpc, function)
        self.assertEqual(expected, returned)

    def test_002_function_echo(self):
        function = echo
        args = ["echo this!"]
        kwargs = {}
        expected = function(*args, **kwargs)
        returned = tr.make_call(self.rpc, function, *args, **kwargs)
        self.assertEqual(expected, returned)

    def test_003_ping(self):
        jrs = '{"method": "ping", "params": null, "id": 0, "jsonrpc": "2.0"}'
        response = self.rpc.execute(jrs)
        response = defaults.json.loads(response["exits"])
        self.assertEqual(response['result'], 'pong')

    def test_005_echo_with_debug(self):
        pseudo_out = PseudoFileHandler()
        self.rpc.debug = True
        previous_out = self.rpc.debug_out
        self.rpc.debug_out = pseudo_out

        self.test_002_function_echo()
        self.rpc.debug = False
        self.rpc.debug_out = previous_out

        self.assertGreater(len(pseudo_out.written), 0)

    def test_010_batch_echo(self):
        rpc = [make_rpc(echo, "one"),
               make_rpc(echo, "two"),
               make_rpc(echo, "three")]
        rpc = defaults.json.dumps(rpc)
        expected = [{"jsonrpc": "2.0", "result": "one"},
                    {"jsonrpc": "2.0", "result": "two"},
                    {"jsonrpc": "2.0", "result": "three"}]

        returned = execute(self.rpc, rpc)
        for entry in returned:
            entry.pop("id")
        self.assertEqual(returned, expected)

    def test_020_notification(self):
        rpc = tr.make_rpc(notification)
        rpc.pop("id") # by not having an id we are a notification
        jsonrpc = defaults.json.dumps(rpc)

        returns = self.rpc.execute(jsonrpc)
        self.assertTrue(returns["calls"][0]["notification"])
        returns = defaults.json.loads(returns["exits"])
        self.assertIsNone(returns)

    def test_025_notification_explicit(self):
        args = ["Removing 'id' makes it a notification regardless of return"]
        rpc = tr.make_rpc(echo, *args)
        rpc.pop("id")
        jsonrpc = defaults.json.dumps(rpc)

        returns = self.rpc.execute(jsonrpc)
        self.assertTrue(returns["calls"][0]["notification"])
        returns = defaults.json.loads(returns["exits"])
        self.assertIsNone(returns)

    def test_027_batch_notification(self):
        # Even if there are multiple notification in a batch it should still
        # be returned as None.
        rpc = [make_rpc(echo, "one"),
               make_rpc(echo, "two"),
               make_rpc(echo, "three")]
        for item in rpc:
            item.pop("id")
        jsonrpc = defaults.json.dumps(rpc)
        returns = self.rpc.execute(jsonrpc)
        self.assertTrue(returns["calls"][0]["notification"])
        returns = defaults.json.loads(returns["exits"])
        self.assertIsNone(returns)

    def test_030_args_and_kwargs(self):
        function = echo
        args = ["nil", "one", "two"]
        kwargs = {"first":True, "second":False}
        returned = tr.make_call(self.rpc, function, *args, **kwargs)
        expected = ["nil one two first:True second:False",
                    "nil one two second:False first:True"]
        self.assertIn(returned, expected)

    def test_035_args_only(self):
        function = echo
        args = ["nil", "one", "two"]
        kwargs = {}
        expected = function(*args, **kwargs)
        returned = tr.make_call(self.rpc, function, *args, **kwargs)
        self.assertEqual(expected, returned)

    def test_036_decorated_data(self):
        function = with_data
        args = ["value of argument"]
        kwargs = {}
        expected = ["value of argument", 'got_data']
        returned = tr.make_call(self.rpc, function, *args, **kwargs)
        self.assertEqual(expected, returned)

    def test_037_with_allow_denied(self):
        function = with_allow_denied
        args = []
        kwargs = {}
        returned = tr.make_call(self.rpc, function, *args, **kwargs)
        self.assertEqual(returned['message'], "Access Denied")

    def test_040_mangled_param(self):
        # The params should always be a structured member like a list or dict
        # However some rpc clients when sending only one parameters do not
        # wrap it in a list, we need to be able to handle that.
        function = echo
        test = "one"
        args = [test]
        kwargs = {}
        json_rpc = tr.make_rpc_json(function, *args, **kwargs)
        json_rpc = json_rpc.replace(' ["one"]', ' "one"')
        result = self.rpc.execute(json_rpc)["exits"]
        result = defaults.json.loads(result)
        self.assertEqual(result["result"], test)

    def test_050_broken_json(self):
        rpc = tr.make_rpc(echo)
        jsonrpc = defaults.json.dumps(rpc)
        # Pretend the last byte is lost in transmission.
        jsonrpc = jsonrpc[:-1]

        result = self.rpc.execute(jsonrpc)["exits"]
        result = defaults.json.loads(result)
        self.assertIn("error", result)
        self.assertEqual(result["error"]["message"], "Parse error")

    def test_051_not_jsonrpc(self):
        jsonrpc = defaults.json.dumps(False)

        result = self.rpc.execute(jsonrpc)["exits"]
        result = defaults.json.loads(result)
        self.assertIn("error", result)
        self.assertEqual(result["error"]["message"], "Invalid Request")

    def test_052_broken_jsonrpc_extra_key(self):
        rpc = tr.make_rpc(echo)
        rpc["illegal"] = "I should not be here"
        jsonrpc = defaults.json.dumps(rpc)

        result = self.rpc.execute(jsonrpc)["exits"]
        result = defaults.json.loads(result)
        self.assertIn("error", result)
        self.assertEqual(result["error"]["message"], "Invalid Request")

    def test_052_broken_jsonrpc_no_version(self):
        rpc = tr.make_rpc(echo)
        rpc.pop("jsonrpc")
        jsonrpc = defaults.json.dumps(rpc)

        result = self.rpc.execute(jsonrpc)["exits"]
        result = defaults.json.loads(result)
        self.assertIn("error", result)
        self.assertEqual(result["error"]["message"], "Invalid Request")

    def test_053_broken_jsonrpc_wrong_version(self):
        rpc = tr.make_rpc(echo)
        rpc["jsonrpc"] = "1.2"
        jsonrpc = defaults.json.dumps(rpc)

        result = self.rpc.execute(jsonrpc)["exits"]
        result = defaults.json.loads(result)
        self.assertIn("error", result)
        self.assertEqual(result["error"]["message"], "Invalid Request")

    def test_054_broken_jsonrpc_no_method(self):
        rpc = tr.make_rpc(echo)
        rpc.pop("method")
        jsonrpc = defaults.json.dumps(rpc)

        result = self.rpc.execute(jsonrpc)["exits"]
        result = defaults.json.loads(result)
        self.assertIn("error", result)
        self.assertEqual(result["error"]["message"], "Invalid Request")

    def test_055_broken_jsonrpc_method_not_found(self):
        rpc = tr.make_rpc("i_dont_exist")
        jsonrpc = defaults.json.dumps(rpc)

        result = self.rpc.execute(jsonrpc)["exits"]
        result = defaults.json.loads(result)
        self.assertIn("error", result)
        self.assertEqual(result["error"]["message"], "Method not found")

    def test_056_broken_jsonrpc_invalid_parameters(self):
        rpc = tr.make_rpc(notification, "method does not have args")
        jsonrpc = defaults.json.dumps(rpc)

        result = self.rpc.execute(jsonrpc)["exits"]
        result = defaults.json.loads(result)
        self.assertIn("error", result)
        self.assertEqual(result["error"]["message"], "Invalid params")

    def test_057_rpc_function_raises_error(self):
        rpc = tr.make_rpc(raise_an_error)
        jsonrpc = defaults.json.dumps(rpc)

        result = self.rpc.execute(jsonrpc)["exits"]
        result = defaults.json.loads(result)
        self.assertIn("error", result)
        self.assertEqual(result["error"]["message"], "Internal error")

    def test_058_rpc_function_raises_error_with_debug(self):
        # This will include a traceback in the error data
        pseudo_out = PseudoFileHandler()
        self.rpc.debug = True
        previous_out = self.rpc.debug_out
        self.rpc.debug_out = pseudo_out

        rpc = tr.make_rpc(raise_an_error)
        jsonrpc = defaults.json.dumps(rpc)
        result = self.rpc.execute(jsonrpc)["exits"]

        self.rpc.debug = False
        self.rpc.debug_out = previous_out

        result = defaults.json.loads(result)
        self.assertIn("error", result)
        self.assertEqual(result["error"]["message"], "Internal error")
        self.assertIn("Traceback (most recent call last):",
                      result["error"]["data"])

    def test_070_batch_one_error(self):
        rpc = [make_rpc(echo, "one"),
               make_rpc(echo, "two"),
               make_rpc(echo, "three"),
               make_rpc(raise_an_error)]

        error_id = None
        for entry in rpc:
            if entry["method"] == "raise_an_error":
                error_id = entry["id"]
        rpc = defaults.json.dumps(rpc)

        error = None
        returned = execute(self.rpc, rpc)
        for entry in returned:
            if entry["id"] == error_id:
                error = entry
            else:
                self.assertIn("result", entry)

        self.assertEqual(error["error"]["message"], "Internal error")

    def test_075_batch_one_json_dump_error(self):
        rpc = [make_rpc(echo, "one"),
               make_rpc(echo, "two"),
               make_rpc(echo, "three"),
               make_rpc(returns_decimal)]

        error_id = None
        for entry in rpc:
            if entry["method"] == "returns_decimal":
                error_id = entry["id"]
        rpc = defaults.json.dumps(rpc)

        error = None
        returned = execute(self.rpc, rpc)
        for entry in returned:
            if entry["id"] == error_id:
                error = entry
            else:
                self.assertIn("result", entry)

        self.assertEqual(error["error"]["message"], "Internal error")

# These forced unhandled errors will only occur when extending the RPC mechanism
# itself.
    def test_080_force_unhandled_exception_dump(self):
        task = _processes.DumpToJson()
        data = dict()
        data["error"] = None
        data["input"] = {"error"}
        data["calls"] = [False,]
        data["batch"] = False
        data["debug"] = False
        data["exits"] = tr.decimal.Decimal(0.01)
        task(data)
        error = defaults.json.loads(data["exits"])
        self.assertEqual(error["error"]["message"], "Internal error")


    def test_081_force_unhandled_exception_buildresponse(self):
        task = _processes.BuildResponse()
        data = dict()
        data["error"] = None
        data["input"] = {"error"}
        data["calls"] = [False,]
        data["batch"] = False
        data["debug"] = False
        data["returns"] = tr.decimal.Decimal(0.01)
        task(data)
        self.assertEqual(data["error"]["message"], "Internal error")
