# Orders/order.py
from enum import Enum

class OrderType(Enum):
    ADD = "AddOrder"
    REDUCE = "ReduceOrder"

class Order:
    def __init__(self, timestamp, order_type, order_id, volume):

        self.timestamp = timestamp
        self.order_type = order_type
        self.order_id = order_id
        self.volume = volume


class AddOrder(Order):
    def __init__(self, timestamp, order_type, order_id, buy_sell, price, volume):
        super().__init__(timestamp, order_type, order_id, volume)
        self.buy_sell = buy_sell
        self.price = price


class ReduceOrder(Order):
    def __init__(self, timestamp, order_type, order_id, volume):
        super().__init__(timestamp, order_type, order_id, volume)
