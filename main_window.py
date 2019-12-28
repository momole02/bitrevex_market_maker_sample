####################################################################
# main_window.py
####################################################################
# Main window implementation
####################################################################
# Project : Bitrevex market maker
# For the Bitrevex Meet Up 1st session
####################################################################

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import re
from datetime import datetime

from settings import *
from bitrevex_interface import *
from market_maker import *
from bot_thread import *

class MainWindow(Tk):

    def __init__(self, parent=None):
        Tk.__init__(self, parent)
        self.title("Bitrevex(R) Market Maker sample")
        self.resizable(False, False)
        #self.geometry("480x320")

        #some tracked widgets elements
        self.tab1=self.tab2=None
        self.image=None
        self.mon_bot_state_label=None
        self.mon_last_order_status_label=None

        #settings  variables
        self.balance_ratio=StringVar()
        self.aggressiveness=DoubleVar()
        self.max_shots=IntVar()
        self.estimated_used_balance=StringVar()
        self.want_asset=StringVar()
        self.offer_asset=StringVar()
        self.api_key=StringVar()
        self.delay_secs=IntVar()
        self.user_data=None

        #monitor variables
        self.mon_bot_state=StringVar()
        self.mon_user=StringVar()
        self.mon_last_update_time=StringVar()
        self.mon_pair=StringVar()
        self.mon_last_balance=StringVar()
        self.mon_last_mid_price=StringVar()
        self.mon_last_spread=StringVar()
        self.mon_last_buy_price=StringVar()
        self.mon_last_sell_price=StringVar()
        self.mon_last_quantity=StringVar()
        self.mon_last_order_status=StringVar()
        self.mon_remaining_shots=StringVar()


        self.bot_ready = False
        self.settings=Settings()
        self.construct_tabs()
        self.construct_tab1()
        self.construct_tab2()
        self.make_bot_unready()
        self.load_settings()

        self.bthread=None
        self.bind('<<Bot_Round>>', self.on_bot_round)
        self.bind('<<Bot_Terminated>>', self.on_bot_terminated)

    def make_bot_unready(self):
        self.update_monitor(bot_state='NOT CONFIGURED', last_update_time='00:00:00',
                            pair='', user='', last_mid_price=0, last_spread=0, last_buy_price=0,
                            last_sell_price=0, last_quantity=0,
                            last_order_status='', remaining_shots=0)
        self.bot_ready=False

    def make_bot_ready(self):
        self.update_monitor(bot_state='READY', last_update_time='00:00:00',
                            user="{}".format(self.user_data['user_email']),
                            pair="{}/{}".format(self.settings.want_asset, self.settings.offer_asset),
                            last_mid_price=0, last_spread=0, last_buy_price=0,
                            last_sell_price=0, last_quantity=0,
                            last_order_status='', remaining_shots=0)
        self.bot_ready=True

    def make_bot_running(self):
        self.update_monitor(bot_state='RUNNING', last_update_time='00:00:00',
                            user="{}".format(self.user_data['user_email']),
                            pair="{}/{}".format(self.settings.want_asset, self.settings.offer_asset),
                            last_mid_price=0, last_spread=0, last_buy_price=0,
                            last_sell_price=0, last_quantity=0,
                            last_order_status='', remaining_shots=0)
        self.bot_ready=True

    def construct_tabs(self):
        notebook = ttk.Notebook(self)
        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        image=PhotoImage(file="assets/logo.gif")
        Label(self, image=image, width=300,height=80).pack(side=TOP)
        self.image=image
        notebook.add(tab1, text="Settings")
        notebook.add(tab2, text="Bot monitoring")
        notebook.pack(expand=1, fill='both')
        self.tab1=tab1
        self.tab2=tab2


    def construct_tab1(self):
        t1=self.tab1

        Label(t1, text="Balance ratio:", anchor=W).grid(row=1, column=0, pady=5, sticky=W)
        self.balance_ratio.set(0.6)
        Entry(t1, textvariable=self.balance_ratio).grid(row=1,column=1)

        Label(t1, text="Max shots:", anchor=W).grid(row=2, column=0, pady=5, sticky=W)
        Spinbox(t1, textvariable=self.max_shots ,from_=2, to=10000).grid(row=2, column=1)

        Label(t1, text="Delay(seconds):" ).grid(row=3, column=0, pady=5, sticky=W)
        Spinbox(t1, textvariable=self.delay_secs, from_=0, to=100).grid(row=3, column=1)

        Label(t1, text="Aggressiveness:" ).grid(row=4, column=0, pady=5, sticky=W)
        Scale(t1, variable=self.aggressiveness , orient=HORIZONTAL, from_=0, to=100, length=150).grid(row=4, column=1)

        Label(t1, text="Left symbol:" ).grid(row=5, column=0, pady=5, sticky=W)
        Entry(t1, textvariable=self.want_asset).grid(row=5, column=1)

        Label(t1, text="Right symbol:").grid(row=6, column=0, pady=5, sticky=W)
        Entry(t1, textvariable=self.offer_asset).grid(row=6, column=1)

        Label(t1, text="Bitrevex API Key:" ).grid(row=7, column=0, pady=5, sticky=W)
        Entry(t1, textvariable=self.api_key).grid(row=7, column=1)

        Button(t1, text="Save settings", command=self.save_settings).grid(row=8, column=0, padx=5, pady=10, sticky=W)

    def construct_tab2(self):
        t2=self.tab2
        self.mon_bot_state_label=Label(t2, textvariable=self.mon_bot_state,relief=RIDGE)
        self.mon_bot_state_label.grid(row=0,column=0,pady=5, sticky=W+E+N+S)
        Label(t2, textvariable=self.mon_pair,relief=RIDGE).grid(row=0,column=1,pady=5,sticky=W+E+N+S)
        Label(t2, textvariable=self.mon_last_mid_price,relief=RIDGE).grid(row=1,column=0,pady=5,sticky=W+E+N+S)
        Label(t2, textvariable=self.mon_last_spread,relief=RIDGE).grid(row=1,column=1,pady=5,sticky=W+E+N+S)
        Label(t2, textvariable=self.mon_last_buy_price,relief=RIDGE,fg="green").grid(row=2,column=0,pady=5,sticky=W+E+N+S)
        Label(t2, textvariable=self.mon_last_sell_price,relief=RIDGE,fg="red").grid(row=2,column=1,pady=5,sticky=W+E+N+S)
        Label(t2, textvariable=self.mon_last_quantity,relief=RIDGE).grid(row=3,column=0,pady=5,sticky=W+E+N+S)
        self.mon_last_order_status_label=Label(t2, textvariable=self.mon_last_order_status,relief=RIDGE)
        self.mon_last_order_status_label.grid(row=5,column=0,pady=5,sticky=W+E+N+S)
        Label(t2, textvariable=self.mon_remaining_shots,relief=RIDGE).grid(row=6,column=0,pady=5,sticky=W+E+N+S)
        Label(t2, textvariable=self.mon_user, fg="blue",relief=RIDGE).grid(row=7,column=0,pady=15,sticky=W+E+N+S)
        Label(t2, textvariable=self.mon_last_update_time, fg="blue",relief=RIDGE).grid(row=8,column=0,pady=5,sticky=W+E+N+S)
        self.start_button=Button(t2, text="Start the bot Now !", command=self.start_bot)
        self.start_button.grid(row=9,column=0,pady=15,sticky=W+E+N+S)

    def verify_settings_stage1(self):
        if  not re.match(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$', self.balance_ratio.get()):
            messagebox.showerror("Market maker", "Verify the balance ratio format")
            return False

        if float(self.balance_ratio.get()) < 1e-4:
            messagebox.showerror("Market maker", "Your balance ratio is too small or null")
            return False


        if float(self.balance_ratio.get()) > 1:
            messagebox.showerror("Market maker", "Your balance ratio must be < 1")
            return False


        if self.max_shots.get() == 0:
            messagebox.showerror("Market maker", "Can't deal with a zero 'max shots' ")
            return False

        if self.aggressiveness.get() == 0:
            messagebox.showerror("Market maker", "Make your bot more aggressive than that !")
            return False

        self.want_asset.set(self.want_asset.get().strip())
        self.offer_asset.set(self.offer_asset.get().strip())
        self.api_key.set(self.api_key.get().strip())

        if self.want_asset.get() == '':
            messagebox.showerror("Market maker", "Enter a valid left symbol")
            return False

        if self.offer_asset.get() == '':
            messagebox.showerror("Market maker", "Enter a valid right symbol")
            return False

        if self.api_key.get() == '':
            messagebox.showerror("Market maker", "Enter a valid Bitrevex(R) API Key")
            return False

        return True

    def verify_settings_stage2(self):
        user_data={}

        try:
            bi = BitrevexInterface('user', self.api_key.get())
            user = bi.callRPCMethod('getUserInfo',{})
            user_data['user_id']=user['user']['id']
            user_data['user_email']=user['user']['email']

        except BitrevexError as e:
            messagebox.showerror("Error", e.message)
            return None
        except Exception as e:
            messagebox.showerror("Error", e.args)
            return None

        return user_data

    def save_settings(self):
        ok_stage1 = self.verify_settings_stage1()
        user_data = self.verify_settings_stage2()
        if ok_stage1 and (user_data is not None):

            self.settings.set(balance_ratio=self.balance_ratio.get(),
                              max_shots=self.max_shots.get(),
                              aggressiveness=self.aggressiveness.get(),
                              want_asset=self.want_asset.get(),
                              offer_asset=self.offer_asset.get(),
                              api_key=self.api_key.get(),
                              delay_secs=self.delay_secs.get())
            self.settings.save()
            self.user_data=user_data
            self.make_bot_ready()
            messagebox.showinfo("Market maker","Your bot is configured successfully")
        else:
            self.make_bot_unready()

    def load_settings(self):
        s = Settings()
        try:
            s.load()
        except Exception as e:
            print(e)

        self.balance_ratio.set(s.balance_ratio)
        self.max_shots.set(s.max_shots)
        self.aggressiveness.set(s.aggressiveness)
        self.want_asset.set(s.want_asset)
        self.offer_asset.set(s.offer_asset)
        self.api_key.set(s.api_key)
        self.delay_secs.set(s.delay_secs)

    def update_monitor(self, **kwargs):
        self.mon_bot_state_label.config(bg="black")
        self.mon_bot_state.set("Bot state: {}".format(kwargs['bot_state']))
        if kwargs['bot_state'] == 'RUNNING':
            self.mon_bot_state_label.config(fg="#00ff00")
        elif kwargs['bot_state'] == 'READY':
            self.mon_bot_state_label.config(fg="#0000ff")
        elif kwargs['bot_state'] == 'STOPPED':
            self.mon_bot_state_label.config(fg="#ff0000")
        else:
            self.mon_bot_state_label.config(fg="white")

        self.mon_last_update_time.set("Last Up time : {}".format(kwargs['last_update_time']))
        self.mon_user.set("Current user: {}".format(kwargs['user']))
        self.mon_pair.set("Pair: {}".format(kwargs['pair']))
        self.mon_last_mid_price.set("Last mid price: {:.8f}".format(kwargs['last_mid_price']))
        self.mon_last_spread.set("Last spread : {:.8f}".format(kwargs['last_spread']))
        self.mon_last_sell_price.set("Last sell price : {:.8f}".format(kwargs['last_sell_price']))
        self.mon_last_buy_price.set("Last buy price: {:.8f}".format(kwargs['last_buy_price']))
        self.mon_last_quantity.set("Last quantity : {:.8f}".format(kwargs['last_quantity']))
        self.mon_last_order_status.set("Last order status : {}".format(kwargs['last_order_status']))
        self.mon_remaining_shots.set("Remaining shots: {}".format(kwargs['remaining_shots']))

    def start_bot(self):
        if self.bot_ready:
            spread_ratio = 1-(self.settings.aggressiveness)/100
            mmaker = MarketMaker(self.settings.want_asset,self.settings.offer_asset,spread_ratio,
                                 float(self.settings.balance_ratio),self.settings.api_key)
            thread=BotThread(self.settings.delay_secs, self.settings.max_shots, mmaker, self)
            thread.start()
            self.bthread=thread
            self.make_bot_running()
            self.start_button.config(state="disabled")

        else:
            messagebox.showerror("Error", "Go to the settings to configure the bot and restart again")

    def on_bot_round(self, data):

       report=self.bthread.report

       self.update_monitor(bot_state='RUNNING', last_update_time=datetime.now().strftime("%H:%M:%S"),
                           user="{}".format(self.user_data['user_email']),
                           pair="{}/{}".format(self.settings.want_asset, self.settings.offer_asset),
                           last_mid_price=report['mid_price'], last_spread=report['spread'],
                           last_buy_price=report['buy_price'],
                           last_sell_price=report['sell_price'], last_quantity=report['quantity'],
                            last_order_status='SUCCESS', remaining_shots=report['remaining_shots'])

    def on_bot_terminated(self, data):
        self.make_bot_ready()
        self.start_button.config(state="normal")
