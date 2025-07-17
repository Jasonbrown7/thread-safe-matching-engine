from dataclasses import dataclass
from enum import Enum, auto
import itertools
import time


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