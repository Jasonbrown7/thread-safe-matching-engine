import unittest
from matching_engine.engine import MatchingEngine


class TestMatchingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = MatchingEngine()

    def test_engine_initialization(self):
        self.assertEqual(self.engine.bids, [])
        self.assertEqual(self.engine.asks, [])
        self.assertEqual(self.engine.orders, {})
        self.assertIsNotNone(self.engine.lock)
