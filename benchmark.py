import time
import random
from matching_engine.engine import MatchingEngine, OrderSide, OrderType

# --- Constants ---
NUM_ORDERS = 100_000
PRICE_MIN = 9900
PRICE_MAX = 10100

def run_benchmark():
    """Instantiates and runs a benchmark on the MatchingEngine."""
    engine = MatchingEngine()

    print("--- Starting Matching Engine Benchmark ---")
    print(f"Submitting {NUM_ORDERS:,} random orders...")

    start_time = time.perf_counter()

    for _ in range(NUM_ORDERS):
        side = random.choice([OrderSide.BUY, OrderSide.SELL])
        order_type = random.choice([OrderType.LIMIT, OrderType.MARKET])
        price = random.randint(PRICE_MIN, PRICE_MAX)
        
        engine.add_order(
            order_type=order_type,
            side=side,
            price=price,
            quantity=10  # Fixed quantity
        )

    end_time = time.perf_counter()

    # --- Performance Metrics ---
    total_time = end_time - start_time
    orders_per_second = NUM_ORDERS / total_time
    avg_latency_micros = (total_time * 1_000_000) / NUM_ORDERS

    print("\n--- Benchmark Results ---")
    print(f"Total Time Elapsed:     {total_time:.4f} seconds")
    print(f"Total Orders Processed: {NUM_ORDERS:,}")
    print("------------------------------------")
    print(f"Throughput:             {orders_per_second:,.2f} orders/sec")
    print(f"Average Latency:        {avg_latency_micros:.2f} µs/order")
    print("------------------------------------\n")

if __name__ == "__main__":
    run_benchmark()
