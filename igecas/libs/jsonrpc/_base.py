# /usr/bin/env false
# -*- coding: UTF-8 -*-

"""
The abstract classes for the processes.
"""
import traceback
# pylint: disable=abstract-class-not-used, abstract-class-little-used

class Process(object):
    """
    Every process is based on this..
    """
    ERROR_CODE = 0
    ERROR_MESSAGE = ""
    EXCEPTIONS = (type('NonExistentError', (ValueError, ), {}),)
    ITERATE_OVER_CALLS = False
    SKIP_ON_ERROR = True

    def process(self, value):
        """
        This function must be implemented by inheritance
        """
        raise NotImplementedError                             # pragma: no cover

    def on_error_data(self, call, exception_instance):
        """
        This function must be implemented by inheritance
        """
        raise NotImplementedError()                           # pragma: no cover

    def _error(self, call, exception_instance):
        """
        This builds the error message in json-rpc struct format.
        """
        error = {"code":self.ERROR_CODE,
                 "message":self.ERROR_MESSAGE}
        data = self.on_error_data(call, exception_instance)
        if data != None:
            error["data"] = data

        return error

    def __call__(self, data):
        """
        Process the task.
        """
        if self.SKIP_ON_ERROR:
            if data["error"] != None:
                data["print"]("! Skipping task due to previous error.")
                return

        # if there is an error in the subtask, skip it.
        if self.ITERATE_OVER_CALLS:
            if data["calls"][data["index"]]["error"] != None:
                return

        try:
            self.process(data)
        except self.EXCEPTIONS as exception_instance:
            trace = traceback.format_exc()
            call = None
            edic = None

            if self.ITERATE_OVER_CALLS:
                index = data["index"]
                call = data["calls"][index]["call"]
                edic = data["calls"][index]
            else:
                call = data["input"]
                edic = data

            edic["error"] = self._error(call, exception_instance)
            if data["debug"]:
                edic["error"]["data"]+= "\n%s" % trace


class PostProcess(Process):
    "Abstract for post process processes as they share the same error handling."
    ERROR_CODE = -32603
    ERROR_MESSAGE = "Internal error"
    EXCEPTIONS = (Exception, )
    SKIP_ON_ERROR = False

    def on_error_data(self, call, exception_instance):
        """
        This error is called when and unknown situation arises.
        """
        text = "Non-handled exception, on call '%s', please contact author."
        return text % call

    def process(self, value):
        """
        This function must be implemented by inheritance
        """
        raise NotImplementedError()                           # pragma: no cover

