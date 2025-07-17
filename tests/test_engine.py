import unittest
from matching_engine.engine import MatchingEngine, OrderSide, OrderType, Trade
import heapq


class TestMatchingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = MatchingEngine()

    def test_engine_initialization(self):
        self.assertEqual(self.engine.bids, [])
        self.assertEqual(self.engine.asks, [])
        self.assertEqual(self.engine.orders, {})
        self.assertIsNotNone(self.engine.lock)

    def test_add_limit_buy_order(self):
        trades = self.engine.add_order(order_type=OrderType.LIMIT, side=OrderSide.BUY, price=100, quantity=10)
        self.assertEqual(trades, [])

        self.assertEqual(self.engine.asks, [])
        self.assertEqual(len(self.engine.bids), 1)
        self.assertEqual(len(self.engine.orders), 1)

        order_id = list(self.engine.orders.keys())[0]
        order = self.engine.orders[order_id]

        self.assertEqual(order.side, OrderSide.BUY)
        self.assertEqual(order.price, 100)
        self.assertEqual(order.quantity, 10)

    def test_simple_limit_buy_order_match(self):
        # Add a resting SELL order
        self.engine.add_order(order_type=OrderType.LIMIT, side=OrderSide.SELL, price=10100, quantity=10)

        # Add an aggressive BUY order that should match
        trades = self.engine.add_order(order_type=OrderType.LIMIT, side=OrderSide.BUY, price=10100, quantity=5)

        # Assert that one trade occurred
        self.assertEqual(len(trades), 1)
        trade = trades[0]

        # Assert the trade details
        self.assertEqual(trade.quantity, 5)
        self.assertEqual(trade.price, 10100)

        # Assert the state of the order books
        self.assertEqual(len(self.engine.bids), 0)  # Aggressive order was fully filled
        self.assertEqual(len(self.engine.asks), 1)  # Resting order should still be on the book

        # Verify the remaining quantity of the resting order
        _, _, _, remaining_quantity = heapq.heappop(self.engine.asks)
        self.assertEqual(remaining_quantity, 5)
