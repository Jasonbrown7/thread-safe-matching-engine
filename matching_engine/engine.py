from dataclasses import dataclass
from enum import Enum, auto
import itertools
import time
import heapq
import threading


class OrderSide(Enum):
    BUY = auto()
    SELL = auto()


class OrderType(Enum):
    LIMIT = auto()
    MARKET = auto()


order_id_generator = itertools.count()


@dataclass(frozen=True)
class Order:
    order_id: int
    side: OrderSide
    order_type: OrderType
    quantity: int
    price: int
    timestamp: int


class MatchingEngine:
    def __init__(self):
        # We store negative prices to simulate a max-heap with Python's min-heap implementation.
        self.bids = []
        self.asks = []
        self.orders = {}
        self.lock = threading.RLock()

    def add_order(self, order_type, side, price, quantity):
        pass

    def cancel_order(self, order_id):
        pass