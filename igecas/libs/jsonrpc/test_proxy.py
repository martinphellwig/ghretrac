# /usr/bin/env false
# _*_ coding: UTF_8 _*_

"""
testing module
"""
# pylint:disable=missing-docstring, too-many-public-methods, invalid-name
# pylint:disable=too-few-public-methods, star-args, unused-argument, no-self-use

import unittest
from . import _proxy
from . import defaults
from requests.packages.urllib3 import exceptions

class _MockSession(object):
    def __init__(self, data, callback):
        self.headers = dict()
        self.content = data
        self.callback = callback

    def post(self, url, data):
        if self.callback != None:
            self.callback(url, data)
        return self

    def __call__(self):
        return self

class _MockRequest(object):
    def __init__(self, result=None, error=None, callback=None, binary=None):
        data = defaults.RESPONSE_OBJECT.copy()
        data['id'] = 1
        if result != None:
            data['result'] = result
        else:
            data['error'] = error

        data = defaults.json.dumps(data)
        data = data.encode(encoding="utf-8")
        if binary != None:
            data = binary
        self.Session = _MockSession(data, callback)


class TestWorks(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self._original_request = _proxy.requests
    
    def tearDown(self):
        _proxy.requests = self._original_request

    def _callback_001(self, url, call):
        call = defaults.json.loads(call)
        self.assertEqual(call, {'jsonrpc': '2.0', 'id': 0, 'method': 'test'})

    def test_001_method_nil(self):
        _proxy.requests = _MockRequest("test", callback=self._callback_001)
        proxy = _proxy.BaseProxy(port='8001', use_tls=True, path='/api/')
        proxy.test()

    def _callback_002(self, url, call):
        call = defaults.json.loads(call)
        self.assertEqual(call, {'jsonrpc': '2.0', 'id': 0, 'method': 'test',
                                'params': ['one']})

    def test_002_method_one(self):
        _proxy.requests = _MockRequest("test", callback=self._callback_002)
        proxy = _proxy.BaseProxy(port='8001', use_tls=True, path='/api/')
        proxy.test("one")

    def _callback_003(self, url, call):
        call = defaults.json.loads(call)
        self.assertEqual(call, {'jsonrpc': '2.0', 'id': 0, 'method': 'test',
                                'params': {'name': 'one'}})

    def test_003_method_kwarg(self):
        _proxy.requests = _MockRequest("test", callback=self._callback_003)
        proxy = _proxy.BaseProxy(port='8001', use_tls=True, path='/api/')
        proxy.test(name="one")

    def _callback_004(self, url, call):
        call = defaults.json.loads(call)
        self.assertEqual(call, {'jsonrpc': '2.0', 'id': 0, 'method': 'test',
                                'params': {'0': 'nil', 'name': 'one'}})

    def test_004_method_arg_kwarg(self):
        _proxy.requests = _MockRequest("test", callback=self._callback_004)
        proxy = _proxy.BaseProxy(port='8001', use_tls=True, path='/api/')
        proxy.test('nil', name="one")

    def _callback_005(self, url, call):
        call = defaults.json.loads(call)
        self.assertEqual(call, {'jsonrpc': '2.0', 'method': 'test'})

    def test_005_method_notification(self):
        _proxy.requests = _MockRequest("test", callback=self._callback_005)
        proxy = _proxy.BaseProxy(port='8001', use_tls=True, path='/api/')
        test = proxy.test
        test.set_notification()
        test()

    def _callback_006(self, url, call):
        call = defaults.json.loads(call)
        self.assertEqual(call, {'jsonrpc': '2.0', 'method': 'test', 'id':0})

    def test_006_method_expect_return(self):
        _proxy.requests = _MockRequest("test", callback=self._callback_006)
        proxy = _proxy.BaseProxy(port='8001', use_tls=True, path='/api/')
        test = proxy.test
        test.set_expect_return_data()
        test()

    def _callback_007(self, url, call):
        call = defaults.json.loads(call)
        self.assertEqual(call, {'jsonrpc': '2.0', 'id': 0,
                                'method': 'test.test'})

    def test_007_method_nil(self):
        _proxy.requests = _MockRequest("test", callback=self._callback_007)
        proxy = _proxy.BaseProxy(port='8001', use_tls=True, path='/api/')
        proxy.test.test()

    def _exception_008(self, *args, **kwargs):
        raise exceptions.ConnectionError('Simulated')

    def test_008_exception(self):
        _proxy.requests = _MockRequest("test")
        proxy = _proxy.BaseProxy(port='8001', use_tls=True, path='/api/')
        test = proxy.test
        test.proxy.__session__.post = self._exception_008
        self.assertRaises(_proxy.JSONRPCERROR, test)

    def _callback_009(self, url, call):
        call = defaults.json.loads(call)
        self.assertEqual(call, {'jsonrpc': '2.0', 'id': 0,
                                'method': 'test'})

    def test_009_method_nil(self):
        binary = chr(1500).encode('utf-32')
        _proxy.requests = _MockRequest("test", callback=self._callback_009,
                                       binary=binary)
        proxy = _proxy.BaseProxy(port='8001', use_tls=True, path='/api/')
        self.assertRaises(_proxy.JSONRPCERROR, proxy.test)

    def _callback_010(self, url, call):
        call = defaults.json.loads(call)
        self.assertEqual(call, {'jsonrpc': '2.0', 'id': 0,
                                'method': 'test'})

    def test_010_method_nil(self):
        error = defaults.INTERNAL_ERROR.copy()
        _proxy.requests = _MockRequest(error=error, callback=self._callback_010)
        proxy = _proxy.BaseProxy(port='8001', use_tls=True, path='/api/')
        self.assertRaises(_proxy.JSONRPCERROR, proxy.test)
