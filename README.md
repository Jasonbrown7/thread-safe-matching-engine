# High-Performance, Thread-Safe Matching Engine

This project is a high-performance, thread-safe order matching engine written in pure Python. It simulates the core functionality of a financial exchange's Central Limit Order Book (CLOB), focusing on performance, correctness, and safe concurrent operations.

This engine was built as a personal project to explore the low-level data structures and concurrency challenges inherent in financial technology systems.

## Core Features
- **Order Types:** Supports both **Limit** and **Market** orders.
- **Operations:** Support for adding and canceling orders.
- **Matching Logic:** Price-time priority matching algorithm.
- **Concurrency:** Designed to be thread-safe for high-concurrency environments.

---

## System Design & Architecture

The design prioritizes performance by selecting data structures that offer the best time complexity for critical operations.

### Data Structures

The core of the engine is a combination of two data structures to manage the order book efficiently:

1.  **Heaps for Price Priority:**
    * The **asks** are stored in a **min-heap**, allowing $O(1)$ access to the best (lowest) ask price.
    * The **bids** are stored in a **max-heap** (implemented by storing negative prices in a min-heap), allowing $O(1)$ access to the best (highest) bid price.
    * This heap-based approach ensures that order insertion and removal are highly efficient, operating at $O(\log n)$ time complexity.

2.  **Dictionary for Fast Lookups:**
    * A separate dictionary (`self.orders`) maps a unique `order_id` to the full `Order` object.
    * This provides constant time, $O(1)$, lookups for order cancellations, avoiding a costly search through the heaps.

### Concurrency Model

To ensure safe operation in a multi-threaded environment where multiple strategies might be submitting or canceling orders simultaneously, the engine employs the following:

* **Reentrant Lock:** All public methods that mutate the engine's state (`add_order`, `cancel_order`) are protected by a single `threading.RLock`. This prevents race conditions and guarantees that the order book's state remains consistent.
* **Lazy Cancellation:** When an order is canceled, it is immediately removed from the `self.orders` dictionary. However, a "ghost" entry may remain in the heap. The matching logic is designed to handle this by simply ignoring any order it pops from the heap if that order's ID is no longer present in the master dictionary. This is an efficient strategy that avoids rebuilding the heap on every cancellation.

---

## Performance Benchmarks

The engine was benchmarked on a multi-core system to validate its performance under concurrent load. The test simulates multiple trading strategies sending orders to the engine simultaneously.

**Test Parameters:**
- **Total Orders:** 200,000
- **Concurrent Threads:** 4
- **Machine:** Apple M3 Pro

**Results:**

| Metric                 | Result                 |
| ---------------------- | ---------------------- |
| **Throughput** | **598,028 orders/sec** |
| **Average Latency** | **1.67 µs / order** |

These results demonstrate the engine's capability to handle a high volume of concurrent orders with extremely low latency, a critical requirement for trading systems.

---

## How to Run

### 1. Setup

Clone the repository and set up a virtual environment:

```bash
git clone <your-repo-url>
cd matching_engine_project
python3 -m venv venv
source venv/bin/activate
```

### 2. Running Tests

The project includes a full suite of unit tests to ensure correctness.

```bash
python3 -m unittest discover -v
```

### 3. Running the Benchmark

To run the multi-threaded performance benchmark:

```bash
python3 benchmark.py
```
