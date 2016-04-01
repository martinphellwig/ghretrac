# /usr/bin/env false
# _*_ coding: UTF_8 _*_

"""
The broker is the main class in this module. The handling of the RPC is defined
as a flow of processes, which are defined in 'PROCESS_FLOW'.
"""
import sys
import pprint
from . import _processes
from . import defaults

PROCESS_FLOW = [
    # Pre-Processing
    _processes.ParseJSON,
    _processes.MakeBatch, # Makes it a batch regardless whether it is or not.

    # Processing
    _processes.VerifyRPC,
    _processes.FindMethod,
    _processes.VerifyAccess,
    _processes.VerifyParameters,
    _processes.ExecuteCall,
    _processes.VerifyOutputCompatibleToJSON,

    # Post-Processing
    _processes.BuildResponse,
    _processes.DumpToJson]


class BaseBroker(object):
    """
    The Broker instance does the main processing flow.
    """
    def __init__(self, check_allow=True, debug=False, out=sys.stderr):
        self.check_allow = check_allow
        self.functions = dict()
        self.login = list()
        self.debug = debug
        self.debug_out = out

    def print(self, data):
        "Debug printer."
        if self.debug:
            text = str(data)
            if not text.endswith("\n"):
                text += "\n"
            self.debug_out.write(text)
            self.debug_out.flush()

    def allow(self, data):       # pylint: disable=no-self-use, unused-argument
        """
        This method is called if a function requires login.
        It must return either True for access allowed or False for access
        denied. Data is the working dictionary.
        """
        return False

    def add(self, function, name=None, check_allow=None):
        "Add a function to the RPC Broker"
        if name == None:
            name = function.__name__

        if check_allow == None:
            check_allow = self.check_allow

        self.functions[name] = {'function':function,
                                'do_check':check_allow}

    def execute(self, jsonrpc_string, begin=None):
        "Execute the JSON-RPC"
        data = defaults.DATA.copy()
        data["input"] = jsonrpc_string
        data["begin"] = begin
        data["names"] = self.functions
        data["debug"] = self.debug
        data["print"] = self.print
        data["allow"] = self.allow

        data["print"]("> Starting execution >")

        for process_class in PROCESS_FLOW:
            process = process_class()
            data["print"]("= stage: %s" % process.__class__.__name__)
            data["print"]("- input: %s" % pprint.pformat(data))

            # Iterative calls can be made in parallel
            if process.ITERATE_OVER_CALLS:
                for index in range(len(data["calls"])):
                    data["index"] = index
                    process(data)
            else:
                process(data)

        data["print"]("- return: %s" % pprint.pformat(data))
        data["print"]("< End Execution <\n")
        return data
