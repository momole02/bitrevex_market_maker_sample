####################################################################
# bitrevex_interface.py
####################################################################
# Bitrevex API helper class
####################################################################
# Project : Bitrevex market maker
# For the Bitrevex Meet Up 1st session
####################################################################

import pycurl, json
from io import BytesIO


class BitrevexError(RuntimeError):
    def __init__(self, arg, status=None):
        self.message=arg
        self.args=arg


class BitrevexInterface:

    '''
    Initialize the bitrevex interface helper
    endpoint : the bitrevex module endpoint
    (Ex : public, funds, user, trade)
    api_key : the bitrevex API key
    '''
    def __init__(self,endpoint, api_key=None):
        self.api_key=api_key
        self.endpoint=endpoint
        self.url = 'http://localhost:8000/api/v1/{}?_key={}'.format(self.endpoint,self.api_key)


    '''
    Call a Bitrevex API JSON RPC method
    method : the method name
    params  : the parameters
    '''
    def callRPCMethod(self, method, params):
        buffer=BytesIO()

        data={
            "jsonrpc":"2.0",
            "id":"1",
            "method":method,
            "params":params
        }

        c=pycurl.Curl()
        c.setopt(c.URL, self.url)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.POSTFIELDS, json.dumps(data))
        c.perform()
        c.close()

        response_data = json.loads(buffer.getvalue().decode('utf-8'))

        if "error" in response_data:
            if "jsonrpc" in response_data :
                raise BitrevexError(response_data['result']['message'], response_data['error'])
            else:
                raise BitrevexError(response_data['result']['message'])

        return response_data['result']