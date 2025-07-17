import time
import random
import threading
from matching_engine.engine import MatchingEngine, OrderSide, OrderType

# --- Constants ---
NUM_THREADS = 4
NUM_ORDERS = 200_000
PRICE_MIN = 9900
PRICE_MAX = 10100

def worker(engine, num_orders_for_thread, barrier):
    """Target function for each thread. Generates and sends a batch of orders."""
    # Wait for all threads to be ready before starting the benchmark
    barrier.wait()

    for _ in range(num_orders_for_thread):
        side = random.choice([OrderSide.BUY, OrderSide.SELL])
        order_type = random.choice([OrderType.LIMIT, OrderType.MARKET])
        price = random.randint(PRICE_MIN, PRICE_MAX)

        engine.add_order(
            order_type=order_type,
            side=side,
            price=price,
            quantity=10  # Fixed quantity
        )

def run_multithreaded_benchmark():
    """Instantiates and runs a multi-threaded benchmark on the MatchingEngine."""
    engine = MatchingEngine()
    
    # A barrier to synchronize the start of all worker threads
    barrier = threading.Barrier(NUM_THREADS)
    
    threads = []
    orders_per_thread = NUM_ORDERS // NUM_THREADS

    print("--- Starting Multi-Threaded Matching Engine Benchmark ---")
    print(f"Using {NUM_THREADS} threads to submit {NUM_ORDERS:,} total orders...")

    for _ in range(NUM_THREADS):
        thread = threading.Thread(
            target=worker,
            args=(engine, orders_per_thread, barrier)
        )
        threads.append(thread)
        thread.start()

    start_time = time.perf_counter()

    for thread in threads:
        thread.join()

    end_time = time.perf_counter()

    # --- Performance Metrics ---
    total_time = end_time - start_time
    orders_per_second = NUM_ORDERS / total_time
    avg_latency_micros = (total_time * 1_000_000) / NUM_ORDERS

    print("\n--- Benchmark Results ---")
    print(f"Test run with:          {NUM_THREADS} threads")
    print(f"Total Time Elapsed:     {total_time:.4f} seconds")
    print(f"Total Orders Processed: {NUM_ORDERS:,}")
    print("------------------------------------")
    print(f"Throughput:             {orders_per_second:,.2f} orders/sec")
    print(f"Average Latency:        {avg_latency_micros:.2f} µs/order")
    print("------------------------------------\n")

if __name__ == "__main__":
    run_multithreaded_benchmark()
