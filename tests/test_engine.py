import unittest
from matching_engine.engine import MatchingEngine, OrderSide, OrderType


class TestMatchingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = MatchingEngine()

    def test_engine_initialization(self):
        self.assertEqual(self.engine.bids, [])
        self.assertEqual(self.engine.asks, [])
        self.assertEqual(self.engine.orders, {})
        self.assertIsNotNone(self.engine.lock)

    def test_add_limit_buy_order(self):
        self.engine.add_order(order_type=OrderType.LIMIT, side=OrderSide.BUY, price=100, quantity=10)

        self.assertEqual(self.engine.asks, [])
        self.assertEqual(len(self.engine.bids), 1)
        self.assertEqual(len(self.engine.orders), 1)

        order_id = list(self.engine.orders.keys())[0]
        order = self.engine.orders[order_id]

        self.assertEqual(order.side, OrderSide.BUY)
        self.assertEqual(order.price, 100)
        self.assertEqual(order.quantity, 10)
