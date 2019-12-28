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


class MainWindow(Tk):

    def __init__(self, parent=None):
        Tk.__init__(self, parent)
        self.title("Bitrevex(R) Market Maker sample")
        #self.geometry("480x320")
        self.construct_tabs()
        self.construct_tab1()
        self.construct_tab2()


    def construct_tabs(self):
        self.notebook = ttk.Notebook(self)
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        image=PhotoImage(file="logo.gif")
        label=Label(self, image=image, width=300,height=80).pack(side=TOP)
        self.image=image
        self.notebook.add(self.tab1, text="Settings")
        self.notebook.add(self.tab2, text="Bot monitoring")
        self.notebook.pack(expand=1, fill='both')

    def construct_tab1(self):
        t1=self.tab1

        Label(t1, text="Balance ratio:", anchor=W).grid(row=1, column=0, pady=5, sticky=W)
        self.balance_ratio_spbox = Spinbox(t1, from_=0.001, to=1)
        self.balance_ratio_spbox.grid(row=1,column=1)

        Label(t1, text="Max shots:", anchor=W).grid(row=2, column=0, pady=5, sticky=W)
        self.balance_ratio_spbox = Spinbox(t1, from_=2, to=10000)
        self.balance_ratio_spbox.grid(row=2, column=1)
        self.balance_estimation_label=Label(t1, text="(Balance estimation)")
        self.balance_estimation_label.grid(row=2, column=2 )

        Label(t1, text="Delay(seconds):" ).grid(row=3, column=0, pady=5, sticky=W)
        self.aggr_ratio_scale = Spinbox(t1, from_=0, to=100)
        self.aggr_ratio_scale.grid(row=3, column=1)

        Label(t1, text="Aggressiveness:" ).grid(row=4, column=0, pady=5, sticky=W)
        self.aggr_ratio_scale = Scale(t1, orient=HORIZONTAL, from_=0, to=100, length=150)
        self.aggr_ratio_scale.grid(row=4, column=1)

        Label(t1, text="Left symbol:" ).grid(row=5, column=0, pady=5, sticky=W)
        self.want_asset_entry = Entry(t1)
        self.want_asset_entry.grid(row=5, column=1)

        Label(t1, text="Right symbol:").grid(row=6, column=0, pady=5, sticky=W)
        self.offer_asset_entry = Entry(t1)
        self.offer_asset_entry.grid(row=6, column=1)

        Label(t1, text="Bitrevex API Key:" ).grid(row=7, column=0, pady=5, sticky=W)
        self.api_key_entry= Entry(t1)
        self.api_key_entry.grid(row=7, column=1)

        Button(t1, text="Save settings").grid(row=8, column=0, padx=5, pady=10, sticky=W)

    def construct_tab2(self):
        t2=self.tab2
        Label(t2, text="Bot state : STOPPED",relief=RIDGE,fg="red", bg="black").grid(row=0,column=0,pady=5, sticky=W+E+N+S)
        Label(t2, text="Pair : ETH/BTC",relief=RIDGE).grid(row=0,column=1,pady=5,sticky=W+E+N+S)
        Label(t2, text="Last Mid price: 0.2400894",relief=RIDGE).grid(row=1,column=0,pady=5,sticky=W+E+N+S)
        Label(t2, text="Last spread: 0.0000944",relief=RIDGE).grid(row=1,column=1,pady=5,sticky=W+E+N+S)
        Label(t2, text="Last buy price: 0.2400794",relief=RIDGE,fg="green").grid(row=2,column=0,pady=5,sticky=W+E+N+S)
        Label(t2, text="Last sell price: 0.2400994",relief=RIDGE,fg="red").grid(row=2,column=1,pady=5,sticky=W+E+N+S)
        Label(t2, text="Last quantity: 8.00",relief=RIDGE).grid(row=3,column=0,pady=5,sticky=W+E+N+S)
        Label(t2, text="Last offer balance: 0.99940",relief=RIDGE).grid(row=4,column=0,pady=5,sticky=W+E+N+S)
        Label(t2, text="Last want balance: 15.40",relief=RIDGE).grid(row=4,column=1,pady=5,sticky=W+E+N+S)
        Label(t2, text="Last order status: SUCCESS",relief=RIDGE,fg="green").grid(row=5,column=0,pady=5,sticky=W+E+N+S)
        Label(t2, text="Remaining shots: 8",relief=RIDGE).grid(row=6,column=0,pady=5,sticky=W+E+N+S)
        Button(t2, text="Start the bot Now !").grid(row=7,column=0,pady=15,sticky=W+E+N+S)