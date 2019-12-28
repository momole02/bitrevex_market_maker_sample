#######################################################################
# settings.py
#######################################################################
# Settings load/save helper
#######################################################################

import json

class Settings:

    def __init__(self):
        self.balance_ratio = 0.01
        self.max_shots = 5
        self.aggressiveness = 50
        self.want_asset = 'ETH'
        self.offer_asset = 'BTC'
        self.api_key = ''
        self.delay_secs = 30

    def set(self,**kwargs):
        self.balance_ratio = kwargs['balance_ratio']
        self.max_shots = kwargs['max_shots']
        self.aggressiveness = kwargs['aggressiveness']
        self.want_asset = kwargs['want_asset']
        self.offer_asset = kwargs['offer_asset']
        self.api_key = kwargs['api_key']
        self.delay_secs = kwargs['delay_secs']
    def get(self):
        return {
            'balance_ratio': self.balance_ratio,
            'max_shots': self.max_shots,
            'aggressiveness': self.aggressiveness,
            'want_asset': self.want_asset,
            'offer_asset': self.offer_asset,
            'api_key': self.api_key,
            'delay_secs': self.delay_secs
        }

    def save(self):
        f=open('settings/settings.json','w')
        f.write(json.dumps({
            'balance_ratio': self.balance_ratio,
            'max_shots': self.max_shots,
            'aggressiveness': self.aggressiveness,
            'want_asset': self.want_asset,
            'offer_asset': self.offer_asset,
            'api_key': self.api_key,
            'delay_secs': self.delay_secs
        }))
        f.close()

    def load(self):
        f=open('settings/settings.json','r')
        data = json.loads(f.read())
        self.balance_ratio=data['balance_ratio']
        self.max_shots=data['max_shots']
        self.aggressiveness=data['aggressiveness']
        self.want_asset=data['want_asset']
        self.offer_asset=data['offer_asset']
        self.api_key=data['api_key']
        self.delay_secs=data['delay_secs']

