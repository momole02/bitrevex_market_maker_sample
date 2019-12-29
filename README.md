# Bitrevex Market Maker Sample

The program here is an simple exemple of a market maker who target Bitrevex Exchange (http://bitrevex.com) 

## Installation

To run the program you must have **python 3** installed. If you don't have the right python version, or you don't have python at all go to the python website https://www.python.org/.

You must also have the following modules :

<ul>
<li><b>tkinter</b> : for the graphical interface, the website is <a href="https://tkdocs.com/tutorial/install.html">https://tkdocs.com/tutorial/install.html</a></li>
<li><b>pyCurl</b> : for the HTTPs REST requests. the website is <a href="http://pycurl.io">http://pycurl.io </a> </li>
</ul>

Once you have installed the modules, go to the program directory :
Create the settings directory : <b>(important)</b>
```bash
mkdir settings
```
and run the main script.

```bash
python __main__.py
```

Or 

```bash
python3 __main__.py
```

 Since I have not error in my source code(i'm sure :lol ), if you got some error verify if you have installed the right modules, if the error persist, post it in the at issues.

## Usage

#### Configure the bot

The first step is to configure the bot, the parameters are : 
 
<ul>
<li><b>Balance ratio</b> : The max ratio of balance you want to use for each order.</li>
<li><b>Max shots</b> :The max numbers of rounds(buy/sell orders). </li>
<li><b>Delay</b> :The delay between each shots(in seconds)</li>
<li><b>Aggressiveness</b>: How much the bot is aggressive, more the bot is agressive, more the orders will shrink the spread.(If you don't understand that read about market maker theory :lol)</li>
<li><b>Left symbol</b> :The left symbol.</li>
<li><b>Right symbol</b> :The right symbol.</li>
<li><b>Bitrevex API Key</b> : Your Bitrevex API Key.</li>
</ul>

Once you have done the configuration, click to "Save settings".
If the configuration is right, you'll have a message who say "The bot is configured successfully".


#### Lauch the bot

Go to the "Bot monitor" tab and start the bot. Some information on this tab is about the last sent order. **Don't forget to have a eye on the console if there are error it's there they will come**. 



## For developers

The important modules are : 
<ul>
<li>bitrevex_interface.py : It contain a good encapsulation of Bitrevex API RPC calls. More info are there: https://github.com/Bitrevex-Exchange/Bitrevex-Official-API</li>
<li>market_maker.py : Contain the computations about the market maker</li>
<li>bot_thread.py : The bot thread, useful to have an overview on the bot functionnng</li>
</ul>

The other modules are not related to bitrevex nor to the market making so there are not too revelant. 
