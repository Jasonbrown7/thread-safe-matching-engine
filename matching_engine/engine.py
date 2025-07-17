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
trade_id_generator = itertools.count()


@dataclass(frozen=True)
class Order:
    order_id: int
    side: OrderSide
    order_type: OrderType
    quantity: int
    price: int
    timestamp: int


@dataclass(frozen=True)
class Trade:
    trade_id: int
    making_order_id: int
    taking_order_id: int
    quantity: int
    price: int


class MatchingEngine:
    def __init__(self):
        # Store negative prices to simulate a max-heap with Python's min-heap implementation
        self.bids = []
        self.asks = []
        self.orders = {}
        self.lock = threading.RLock()

    def add_order(self, order_type, side, price, quantity) -> tuple[int, list["Trade"]]:
        trades = []
        with self.lock:
            order_id = next(order_id_generator)
            timestamp = time.time_ns()
            taking_order = Order(order_id, side, order_type, quantity, price, timestamp)
            self.orders[order_id] = taking_order

            if side == OrderSide.BUY:
                while self.asks and taking_order.quantity > 0 and taking_order.price >= self.asks[0][0]:
                    maker_price, maker_ts, maker_id, maker_qty = heapq.heappop(self.asks)
                    if maker_id not in self.orders:
                        continue
                    making_order = self.orders.pop(maker_id)

                    trade_quantity = min(taking_order.quantity, making_order.quantity)
                    trade_price = making_order.price
                    trades.append(Trade(next(trade_id_generator), maker_id, order_id, trade_quantity, trade_price))

                    # Update the aggressive (taking) order
                    new_taking_quantity = taking_order.quantity - trade_quantity
                    taking_order = Order(order_id, side, order_type, new_taking_quantity, price, timestamp)
                    self.orders[order_id] = taking_order

                    # If the resting (making) order is not fully filled, put it back
                    if making_order.quantity > trade_quantity:
                        remaining_maker_quantity = making_order.quantity - trade_quantity
                        new_making_order = Order(maker_id, making_order.side, making_order.order_type, remaining_maker_quantity, making_order.price, making_order.timestamp)
                        self.orders[maker_id] = new_making_order
                        heapq.heappush(self.asks, (new_making_order.price, new_making_order.timestamp, new_making_order.order_id, new_making_order.quantity))
                
                if taking_order.quantity > 0:
                    self.orders[order_id] = taking_order
                    heapq.heappush(self.bids, (-taking_order.price, taking_order.timestamp, taking_order.order_id, taking_order.quantity))
                else:
                    del self.orders[order_id]

            else:  # side == OrderSide.SELL
                while self.bids and taking_order.quantity > 0 and taking_order.price <= -self.bids[0][0]:
                    _, maker_ts, maker_id, maker_qty = heapq.heappop(self.bids)
                    if maker_id not in self.orders:
                        continue
                    making_order = self.orders.pop(maker_id)

                    trade_quantity = min(taking_order.quantity, making_order.quantity)
                    trade_price = making_order.price
                    trades.append(Trade(next(trade_id_generator), maker_id, order_id, trade_quantity, trade_price))

                    new_taking_quantity = taking_order.quantity - trade_quantity
                    taking_order = Order(order_id, side, order_type, new_taking_quantity, price, timestamp)
                    self.orders[order_id] = taking_order

                    if making_order.quantity > trade_quantity:
                        remaining_maker_quantity = making_order.quantity - trade_quantity
                        new_making_order = Order(maker_id, making_order.side, making_order.order_type, remaining_maker_quantity, making_order.price, making_order.timestamp)
                        self.orders[maker_id] = new_making_order
                        heapq.heappush(self.bids, (-new_making_order.price, new_making_order.timestamp, new_making_order.order_id, new_making_order.quantity))

                if taking_order.quantity > 0:
                    self.orders[order_id] = taking_order
                    heapq.heappush(self.asks, (taking_order.price, taking_order.timestamp, taking_order.order_id, taking_order.quantity))
                else:
                    del self.orders[order_id]

            return (order_id, trades)

    def cancel_order(self, order_id):
        with self.lock:
            if order_id in self.orders:
                del self.orders[order_id]
                return True
            return False