######################################################
# bot_thread.py
######################################################
# Main bot thread
######################################################

import threading
import time
from market_maker import *


class BotThread(threading.Thread):
    '''
    Create a new market maker bot thread
    delay : delay between order sending signals
    max_shots : number of signats to send
    mmaker : a full initialized market maker
    '''
    def __init__(self, delay, max_shots, mmaker ):
        threading.Thread.__init__(self)
        self.delay = delay
        self.max_shots = max_shots
        self.mmaker = mmaker
        self.last_shot_time = time.time()

    '''
    Bot thread entry point
    '''
    def run(self):

        remaining_shots=self.max_shots
        print("[MarketMaker thread] thread started")
        while remaining_shots>0:
            tm=time.time()

            if tm-self.last_shot_time >= self.delay:
                try:
                    print("[MarketMaker thread] sending order...")

                    report = self.mmaker.sendOrder()
                    remaining_shots -= 1

                    print("[MarketMaker thread] order sent (remaining shots : {} )!".format(remaining_shots))
                    print("Spread = {:.8f} , Buy price={:.8f} , Sell price={:.8f} , Mid price={:.8f}".format(
                        report['spread'],
                        report['buy_price'],
                        report['sell_price'],
                        report['mid_price']
                    ))

                except MarketMakerError as err:
                    print("[MarketMaker thread] error : ", err.message, err.api_message)

                except Exception as err:
                    print("[MarketMaker thread] unexpected error : ", err.args)
                    break
                finally:
                    self.last_shot_time = time.time()
