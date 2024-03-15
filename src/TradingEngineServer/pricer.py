from sortedcontainers import SortedDict


def custom_sort_key(string):
    return -float(string) if string else float('-inf')


class OrderBook:

    def __init__(self):
        self.bids = SortedDict(custom_sort_key)  # List to store bid orders
        self.bids_total_size = 0
        self.asks = SortedDict()  # List to store ask orders
        self.asks_total_size = 0
        self.expense = 0
        self.income = 0

    def process_add_order(self, locator, order_id, buy_or_sell, price, size):
        """
                Add an order to the order book.

                Parameters:
                - locator: Dictionary to track order details.
                - order_id: Unique identifier for the order.
                - buy_or_sell: 'B' for buy order, 'S' for sell order.
                - price: Price of the order.
                - size: Size of the order.
        """
        if buy_or_sell == 'B':
            if str(price) not in self.bids.keys():
                self.bids[str(price)] = {}
            self.bids[str(price)][order_id] = size
            self.bids_total_size += size

        elif buy_or_sell == 'S':
            if str(price) not in self.asks.keys():
                self.asks[str(price)] = {}
            self.asks[str(price)][order_id] = size
            self.asks_total_size += size

        else:
            raise Exception ("Wrong order type sent")

        locator[order_id] = [price, buy_or_sell]

    def display_order_book(self):
        """
                Display the current state of the order book.
        """
        print("Currently Order book looks like:\n")
        print("Bids Book:")

        for price, order_details in self.bids.items():
            for order_id, size in order_details.items():
                print(f"Bid Price: {price}, Order-id: {order_id}, Size: {size}")

        print("Asks Book:")

        for price, order_details in self.asks.items():
            for order_id, size in order_details.items():
                print(f"Ask Price: {price}, Order-id: {order_id}, Size: {size}")

    def process_reduce_order(self, locator, order_id, size):
        """
                Reduce the size of an existing order in the order book.

                Parameters:
                - locator: Dictionary to track order details.
                - order_id: Unique identifier for the order.
                - size: Size to reduce from the order.
        """
        price, buy_or_sell = locator[order_id]
        if buy_or_sell == "B":
            self.bids[str(price)][order_id] -= size
            self.bids_total_size -= size
            if self.bids[str(price)][order_id] <= 0:
                self.bids[str(price)][order_id] = 0
            if self.bids_total_size < 0:
                raise Exception("Reduce orders tried to remove more bids size than possible")

        else:
            self.asks[str(price)][order_id] -= size
            self.asks_total_size -= size
            if self.asks[str(price)][order_id] <= 0:
                self.asks[str(price)][order_id] = 0
            if self.asks_total_size < 0:
                raise Exception("Reduce orders tried to remove more ask size than possible")

    def calculate_expense_income(self, locator, order_id, target_size):
        """
                Calculate expense and income based on the order book.

                Parameters:
                - locator: Dictionary to track order details.
                - order_id: Unique identifier for the order.
                - target_size: Target size for buying or selling.

                Returns:
                - Tuple containing expense and income.
        """
        expense = 0
        income = 0
        amount_left = target_size
        _, buy_or_sell = locator[order_id]
        if buy_or_sell == "B":
            if self.bids_total_size >= amount_left:
                for price, order in self.bids.items():
                    for order_id, size in order.items():
                        if size != 0:
                            income += min(amount_left, size) * float(price)
                            can_cut = min(amount_left, size)
                            amount_left -= can_cut
                            if amount_left == 0:
                                break
                    if amount_left == 0:
                        break

        if buy_or_sell == "S":
            if self.asks_total_size >= amount_left:
                for price, order in self.asks.items():
                    for order_id, size in order.items():
                        if size != 0:
                            expense += min(amount_left, size) * float(price)
                            amount_left -= min(amount_left, size)
                            if amount_left == 0:
                                break
                    if amount_left == 0:
                        break

        expense_return = "NO-OP"
        income_return = "NO-OP"

        if buy_or_sell == "B":
            if income != self.income:
                if income == 0:
                    income_return = 'NA'
                else:
                    income_return = income
                self.income = income
        else:
            if expense != self.expense:
                if expense == 0:
                    expense_return = 'NA'
                else:
                    expense_return = expense
                self.expense = expense

        # print("self.bids size = ", self.bids_total_size, "self.asks size = ", self.asks_total_size)
        # print("self.expense = ", self.expense, "self.income = ", self.income)
        # print("expense = ", expense, "income = ", income)
        # print("expense return = ", expense_return, "income return = ", income_return)
        return expense_return, income_return


def main(target_size):
    order_book = OrderBook()
    # fz = os.path.abspath(__file__)
    # file_path = os.path.join(fz, "../market_data.log")
    x = "/Users/akhilvaid/Desktop/Uchicago 2023/intermediatePythonProgramming/projectFinal/final-project-codesniper99/src/TradingEngineServer"
    locator = {}

    with open(x+"/market_data.log", 'r') as file:
        for line in file:
            # try:
            fields = line.strip().split()

            timestamp = int(fields[0])
            message_type = fields[1]
            order_id = fields[2]

            if message_type == 'A':
                buy_or_sell = fields[3]
                price = fields[4]
                size = fields[5]
                order_book.process_add_order(locator, order_id, buy_or_sell, float(price), int(size))

            elif message_type == 'R':
                size = fields[3]
                order_book.process_reduce_order(locator, order_id, int(size))

            # print("After reading ", fields, "The Orderbook looks like")
            # order_book.display_order_book()

            expense, income = order_book.calculate_expense_income(locator, order_id, target_size)

            # if expense != 'NO-OP':
            #     # print(f"{timestamp} B {expense}")
            #
            # if income != 'NO-OP':
            #     # print(f"{timestamp} S {income}")
            # print("======================")
            # except Exception as e:
            #     print(f"Error processing message: {line.strip()}. {str(e)}", file=sys.stderr)


if __name__ == "__main__":
    main(200)
    # if len(sys.argv) != 2:
    #     print("Usage: python Pricer.py <target-size>")
    #     sys.exit(1)
    #
    # try:
    #     target_size = int(sys.argv[1])
    #     main(target_size)
    # except ValueError:
    #     print("Invalid target size. Please provide a valid integer.", file=sys.stderr)
    #     sys.exit(1)