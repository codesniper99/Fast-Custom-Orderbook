
import threading
import time
import os
from pricer import OrderBook
from Logging.abstract_logger import Log, LogLevel
from Orders.orders import OrderType, AddOrder, ReduceOrder
from datetime import datetime


class TradingEngine:
    def __init__(self):
        self.order_book = OrderBook()
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.main_log_file = f"main_log_{current_time}.txt"
        self.orderbook_log_file = f"orderbook_{current_time}.txt"

        self.order_folder = "orders"
        self.instrument_file = "../Instrument/instruments.txt"  # Path to the instrument file
        self.exit_flag = False
        self.main_thread = threading.Thread(target=self.main_loop)
        self.order_thread = threading.Thread(target=self.order_listener)
        self.log = Log(self.main_log_file)
        self.orderbook_log = Log(self.orderbook_log_file)
        self.locator = {}
        self.target_size = 200

    def main_loop(self):
        self.log.log(LogLevel.INFO, "Main Thread: Running...")

        while not self.exit_flag:
            # Your main trading logic goes here
            self.log_order_book()
            time.sleep(1)  # Placeholder for your main trading logic

    def log_order_book(self):
        """
                Log the current state of orderbook
        """
        # Opening the file in write mode, which clears its contents
        with open(self.orderbook_log_file, "w"):
            pass  # empty so that we clear it at each stage

        self.orderbook_log.info("Currently Order book looks like:\n")
        self.orderbook_log.info("Bids Book:")

        for price, order_details in self.order_book.bids.items():
            for order_id, size in order_details.items():
                self.orderbook_log.info(f"Bid Price: {price}, Order-id: {order_id}, Size: {size}")

        self.orderbook_log.info("Asks Book:")

        for price, order_details in self.order_book.asks.items():
            for order_id, size in order_details.items():
                self.orderbook_log.info(f"Ask Price: {price}, Order-id: {order_id}, Size: {size}")

    def process_order(self, order_data, order_file):

        # Parse the data
        timestamp = int(order_data[0])
        order_type = order_data[1]
        order_id = order_data[2]

        if order_type == 'A':
            buy_or_sell = order_data[3]
            price = order_data[4]
            size = order_data[5]
            order = AddOrder(timestamp, OrderType.ADD, order_id, buy_or_sell, price, size)
            self.order_book.process_add_order(self.locator, order_id, buy_or_sell, float(price), int(size))
            self.log_order_info(order)

        elif order_type == 'R':
            size = order_data[3]
            order = ReduceOrder(timestamp, OrderType.REDUCE, order_id, size)
            self.order_book.process_reduce_order(self.locator, order_id, int(size))
            self.log_order_info(order)
        else:
            error_message = f"Error with processing file '{order_file}': Unsupported order type '{order_type}'."
            self.log.log(LogLevel.ERROR, error_message)
            return False

        expense, income = self.order_book.calculate_expense_income(self.locator, order_id, self.target_size)
        # print("Order id: ", order_id, " expense ", expense, " income ", income)
        self.log_expense_income_info(expense, income, timestamp)
        return True

    def log_expense_income_info(self, expense, income, timestamp):
        if expense != 'NO-OP':
            log_message = (f"After receiving Ask order with {timestamp}, we can Buy {self.target_size} shares for"
                           f" {expense}")

            self.log.log(LogLevel.INFO, log_message)

        if income != 'NO-OP':
            log_message = (f"After receiving Bid order with {timestamp}, we can Sell {self.target_size} shares for"
                           f" {income}")

            self.log.log(LogLevel.INFO, log_message)

    def get_instrument_info(self, symbol):
        with open(self.instrument_file, "r") as f:
            for line in f:
                instrument_data = line.strip().split(",")
                if len(instrument_data) == 3 and instrument_data[0] == symbol:
                    return instrument_data
        return None

    def log_order_info(self, order):
        if isinstance(order, AddOrder):
            log_message = (f"AddOrder: Timestamp={order.timestamp}, "
                           f"OrderID={order.order_id},"
                           f" Buy/Sell={order.buy_sell},"
                           f" Bid/Ask={order.price}, Volume={order.volume},")
        elif isinstance(order, ReduceOrder):
            log_message = (f"ReduceOrder: Timestamp={order.timestamp},"
                           f" OrderID={order.order_id}, Volume={order.volume},")
        else:
            log_message = f"Unsupported order type: {type(order).__name__}"

        self.log.info(log_message)

    def order_listener(self):
        processed_orders_folder = "processed_orders"  # New directory name

        # Create the processed_orders folder if it doesn't exist
        if not os.path.exists(processed_orders_folder):
            os.makedirs(processed_orders_folder)

        while not self.exit_flag:
            order_files = [f for f in os.listdir(self.order_folder) if f.endswith(".txt")]

            for order_file in order_files:
                order_path = os.path.join(self.order_folder, order_file)
                success = True
                with open(order_path, "r") as f:
                    individual_order = f.read().strip().split('\n')
                    # print(individual_order)
                    for order in individual_order:
                        order_data = order.strip().split()
                        if len(order_data) == 6 or len(order_data) == 4:
                            result = self.process_order(order_data, order_file)
                            success = success and result
                        elif len(order_data) > 0:
                            # Log an error message indicating the file name and the reason
                            error_message = (f"Error processing file '{order_file}': "
                                             f"Expected 6 or 4 arguments, but found "
                                             f"{len(order_data)}.")
                            self.log.log(LogLevel.ERROR, error_message)
                            success = False
                        else:
                            success = False

                # Process the order, passing order_file as an argument
                # Remove the processed order file
                if success:
                    self.log.info(f"Successfully processed order file:  {order_file}")
                    processed_order_path = os.path.join(processed_orders_folder, order_file)
                    try:
                        os.replace(order_path, processed_order_path)
                        self.log.info(f"Moved {order_file} to processed_orders.")

                    except Exception as e:
                        error_message = f"Error moving {order_file} to processed_orders: {e}"
                        self.log.log(LogLevel.ERROR, error_message)
        time.sleep(1)  # Adjust this based on how frequently you want to check for new orders

    def start(self):
        # Start both threads
        print("Starting Trading Engine Server...")
        self.main_thread.start()
        self.order_thread.start()

        try:
            # Wait for Ctrl+C to stop the main thread
            self.main_thread.join()
        except KeyboardInterrupt:
            print("Stopping threads...")
            info_message = f"Stopping threads..."
            self.log.log(LogLevel.INFO, info_message)
            self.exit_flag = True
            self.main_thread.join()
            self.order_thread.join()
            print("Threads stopped.")
            info_message = f"Threads stopped."
            self.log.log(LogLevel.INFO, info_message)


if __name__ == "__main__":
    trading_engine = TradingEngine()
    trading_engine.start()
