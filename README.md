
# Trading Engine Server - Orderbook

Name: Akhil Vaid
cnet: avaid

Google Drive link for data: [All Data required](https://drive.google.com/drive/folders/1M-zieybOf5Zn_fJ1mBcUIIJ4zugBEDp1?usp=sharing)


I have implemented a Trading Engine Server in Python, along with a custom Logging Level implementation. This interests me as I have wanted to break into financial code development
and incorporate my Python learnings with this. Specifically I implemented an Orderbook functionality.

**This mimics incoming Bid and Ask orders in a market**. For a given Target size we then calculate the amount of expense/income I can generate 
by buying/selling target_size amount of shares at the moment a new order comes in. This depends how intelligently we choose 
highest bids for maximizing income and lowest asks to minimize expense.

The complexity in the challenge is being able to handle upto million operations efficiently, which we do 
using SortedDict which uses Red-black tree for keeping a dict sorted based on its key. Thus,
Operations like insert take O(log n) and Delete take O(1).

This implementation also mimics how a multimap works in languages like C++/Java, but isnt present for Python,
I immensely enjoyed creating this project and believe there is much scope of improvement and extending this both horizontally by
adding more threads or vertically by using more compute power.

I believe the current bottleneck to performance is the logging system, as to process the big_order.txt it takes almost 1 hour to fully
write all the important info loglines to main_log. You can see this if you check the `main_log_2023-12-03_19-42-32.txt`
provided in the google drive link. 

I think this can spur an important discussion over how much information should be logged and not. Would love to discuss this with the
professor but in the meantime, I have logged relevant info as efficiently as possible.



I have chosen the following as my Problem statement:

## Problem Statement
Better description can be found here: 
[Reviwer Read this](https://htmlpreview.github.io/?https://github.com/panaali/orderbook/blob/master/problem.html)


Suppose your great aunt Gertrude dies and leaves you $3000 which you decide you want to invest in the Acme Internet Widget Company (stock symbol:AIWC). You are willing to pay up to $30 per share of AIWC. So you log in to your online trading account and enter a limit order: "BUY 100 AIWC @ $30". It's a limit order because that's most you're willing to pay. You'd be willing to pay less than $30, but not more than $30. Your order will sit around in the market until you get your 100 shares. A limit order to buy is called a "bid".

But you're not the only prospective buyer for AIWC stock. Others want to buy it too. One is bidding $31/share for 200 shares, while another is bidding $29/share for 300 shares. When Warren Buffett wants to sell 225 shares, he's obviously going to take the highest price he can get for each share. So he hits the $31 bid first, selling 200 shares. Then he sells his remaining 25 shares to you at $30/share. Your bid size reduced by 25, leaving 75 shares still to be bought.

Suppose you eventually get the full 100 shares at some price. Next year, you decide to buy a new computer and you need $4500 for it, and luckily the value of AIWC has appreciated by 50%. So you want to sell your 100 shares of AIWC stock for at least $45/share. So you enter this limit order: "SELL 100 AIWC @ $45". A limit order to sell is called an "ask".

But you're not the only prospective seller of AIWC stock. There's also an ask for $44/share and an ask for $46/share. If Alan Greenspan wants to buy AIWC, he's obviously going to pay as little as possible. So he'll take the $44 offer first, and only buy from you at $45 if he can't buy as much as he wants at $44.

The set of all standing bids and asks is called a "limit order book", or just a "book". You can buy a data feed from the stock market, and they will send you messages in real time telling you about changes to the book. Each message either adds an order to the book, or reduces the size of an order in the book (possibly removing the order entirely). You can record these messages in a log file, and later you can go back and analyze your log file.

## Problem
Your task is to write a program, Pricer, that analyzes such a log file. Pricer takes one command-line argument: target-size. Pricer then reads a market data log on standard input. As the book is modified, Pricer prints (on standard output) the total expense you would incur if you bought target-size shares (by taking as many asks as necessary, lowest first), and the total income you would receive if you sold target-size shares (by hitting as many bids as necessary, highest first). Each time the income or expense changes, it prints the changed value.


## Solution
We wrote a program, where if you add text files in the src/TradingEngineServer/orders then it processes them and sends them to processed order.
Along with this a record for each processed order is maintained in the main_log_file it creates and to view the orderbook at any time you can check the orderbook_log{current time}.txt file

We use sorted Dict which helps with a Red-Black tree implementation.

## How to run
run the trading_engine_Server.py file normally as you would
`python3 trading_engine_server.py`

I don't think there are any requirements of external modules other than `sortedcontainers`

You can use the data I provide as order*.txt in the google drive and move them sequentially into the orders folder present in
TradingEngineServer directory.

You are free to create your own orders as well to mimic the orderbook add and reduce orders as per the input format in the 
problem statement linked. 


Monitor the directory you are running for the output log files as:
1. main_log_{current_time}.txt
2. orderbok_{current_time}.txt
