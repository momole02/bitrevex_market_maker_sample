
# from market_maker import *
# from bot_thread import *
#
# try:
#     mm = MarketMaker('SPZ', 'BTC', 0.03, 0.2, '610fbefbf2dd84e89d70c570311214294547d2b9992be085526a781c09a9487a')
#
#     bot = BotThread(10, 3, mm)
#     bot.start()
#
# except MarketMakerError as err:
#     print(err.message , err.api_message)
# except Exception as err:
#     print(err.args)

from main_window import *

MainWindow().mainloop()
