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
        # Store negative prices to simulate a max-heap with Python's min-heap implementation
        self.bids = []
        self.asks = []
        self.orders = {}
        self.lock = threading.RLock()

    def add_order(self, order_type, side, price, quantity):
        with self.lock:
            order_id = next(order_id_generator)
            timestamp = time.time_ns()

            order = Order(
                order_id=order_id,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price,
                timestamp=timestamp,
            )

            self.orders[order.order_id] = order

            if side == OrderSide.BUY:
                heapq.heappush(
                    self.bids, (-order.price, order.timestamp, order.order_id, order.quantity)
                )
            else:  # side == OrderSide.SELL
                heapq.heappush(
                    self.asks, (order.price, order.timestamp, order.order_id, order.quantity)
                )

    def cancel_order(self, order_id):
        pass