"""
Assignment 1 – Producer-Consumer with Thread Synchronization

This program demonstrates the producer-consumer pattern using Python threads.
It uses a bounded buffer where producers add items and consumers remove them.
Synchronization between threads is handled using Locks and Condition variables.
The design supports multiple producers and consumers and runs quickly without using sleep().
"""

import threading
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Generic, Iterable, List, Optional, TypeVar

T = TypeVar("T")


class BoundedBuffer(Generic[T]):
    """A simple thread-safe bounded queue using Conditions for synchronization."""

    def __init__(self, maxsize: int):
        self._maxsize = maxsize
        self._buf: Deque[T] = deque()
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)
        self._not_full = threading.Condition(self._lock)
        self._closed = False

    def put(self, item: T) -> None:
        """Add an item to the buffer, waiting if it’s full."""
        with self._not_full:
            while len(self._buf) >= self._maxsize and not self._closed:
                self._not_full.wait()
            if self._closed:
                raise RuntimeError("Cannot put into closed buffer")
            self._buf.append(item)
            self._not_empty.notify()

    def get(self) -> Optional[T]:
        """Remove and return an item, waiting if the buffer is empty."""
        with self._not_empty:
            while True:
                if self._buf:
                    item = self._buf.popleft()
                    self._not_full.notify()
                    return item
                if self._closed:
                    return None
                self._not_empty.wait()

    def close(self) -> None:
        """Close the buffer and wake all waiting threads."""
        with self._lock:
            self._closed = True
            self._not_empty.notify_all()
            self._not_full.notify_all()


@dataclass
class Producer(Generic[T]):
    """Produces items from a source iterable and adds them to the buffer."""
    source: Iterable[T]
    buffer: BoundedBuffer[T]

    def run(self) -> None:
        for item in self.source:
            self.buffer.put(item)
        # The buffer will be closed externally after all producers finish.


@dataclass
class Consumer(Generic[T]):
    """Consumes items from the buffer until it is closed."""
    buffer: BoundedBuffer[T]
    dest: List[T] = field(default_factory=list)

    def run(self) -> None:
        while True:
            item = self.buffer.get()
            if item is None:
                break
            self.dest.append(item)


def run_scenario(name: str, data: list):
    """Run a simple producer-consumer scenario with one producer and one consumer."""
    buf = BoundedBuffer(maxsize=10)
    consumer = Consumer(buffer=buf)
    producer = Producer(source=data, buffer=buf)

    t_prod = threading.Thread(target=producer.run)
    t_cons = threading.Thread(target=consumer.run)
    t_prod.start()
    t_cons.start()

    t_prod.join()
    buf.close()  # Close the buffer after producer finishes
    t_cons.join()

    print(f"{name}: produced={len(data)}, consumed={len(consumer.dest)}")


def demo_fast():
    """Demonstrates different data types and a multi-producer scenario."""
    import random
    from dataclasses import dataclass

    print("=== Fast Producer-Consumer Demo ===")

    dict_data = [{"id": i, "value": random.random()} for i in range(20)]
    tuple_data = [(i, f"task-{i}") for i in range(20)]

    @dataclass
    class Order:
        order_id: int
        total: float

    order_data = [Order(i, i * 1.1) for i in range(10)]

    nested_data = [
        {"user": {"id": i}, "events": [{"t": j} for j in range(2)]}
        for i in range(10)
    ]

    # Single-producer examples
    run_scenario("Dict Data", dict_data)
    run_scenario("Tuple Data", tuple_data)
    run_scenario("Dataclass Orders", order_data)
    run_scenario("Nested JSON", nested_data)

    # Multi-producer example
    print("\n--- Multi-Producer Test ---")
    chunks = [list(range(i * 10, (i + 1) * 10)) for i in range(3)]
    buf = BoundedBuffer[int](maxsize=5)
    consumer = Consumer[int](buffer=buf)
    producers = [Producer[int](source=chunk, buffer=buf) for chunk in chunks]

    prod_threads = [threading.Thread(target=p.run) for p in producers]
    cons_thread = threading.Thread(target=consumer.run)

    for t in prod_threads:
        t.start()
    cons_thread.start()

    for t in prod_threads:
        t.join()
    buf.close()
    cons_thread.join()

    total_produced = sum(len(chunk) for chunk in chunks)
    print(f"Total produced: {total_produced}, consumed: {len(consumer.dest)}")


if __name__ == "__main__":
    demo_fast()
