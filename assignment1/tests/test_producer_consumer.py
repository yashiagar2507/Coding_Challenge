"""
Assignment 1 – Unit Tests for Producer–Consumer

This file contains unit tests that verify the behavior of the
Producer–Consumer implementation in `assignment1/producer_consumer.py`.
Each test checks a different part of the system such as blocking,
ordering, and performance.
"""

import unittest
import threading
import time
from dataclasses import dataclass
from assignment1.producer_consumer import BoundedBuffer, Producer, Consumer


class TestProducerConsumer(unittest.TestCase):
    """Unit tests for the Producer–Consumer system."""

    def test_basic_roundtrip(self):
        """Single producer and single consumer transfer data correctly."""
        data = list(range(100))
        buf = BoundedBuffer[int](maxsize=10)
        consumer = Consumer[int](buffer=buf)
        producer = Producer[int](source=data, buffer=buf)

        t_prod = threading.Thread(target=producer.run)
        t_cons = threading.Thread(target=consumer.run)
        t_prod.start()
        t_cons.start()
        t_prod.join()
        buf.close()
        t_cons.join()

        self.assertEqual(consumer.dest, data)

    def test_buffer_blocking_behavior(self):
        """Producer waits when buffer is full, consumer unblocks it."""
        buf = BoundedBuffer[int](maxsize=2)
        result = []

        def producer_task():
            for i in range(5):
                buf.put(i)
            buf.close()

        def consumer_task():
            while True:
                item = buf.get()
                if item is None:
                    break
                result.append(item)

        t1 = threading.Thread(target=producer_task)
        t2 = threading.Thread(target=consumer_task)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        self.assertEqual(result, list(range(5)))

    def test_complex_data_types(self):
        """Check that buffer handles dicts, tuples, and dataclass objects."""

        @dataclass
        class Item:
            id: int
            name: str

        data = (
            [{"id": i} for i in range(10)]
            + [(i, f"v{i}") for i in range(10)]
            + [Item(i, f"n{i}") for i in range(10)]
        )

        buf = BoundedBuffer(maxsize=5)
        consumer = Consumer(buffer=buf)
        producer = Producer(source=data, buffer=buf)

        t1 = threading.Thread(target=producer.run)
        t2 = threading.Thread(target=consumer.run)
        t1.start()
        t2.start()
        t1.join()
        buf.close()
        t2.join()

        self.assertEqual(consumer.dest, data)

    def test_put_after_close_raises(self):
        """Adding to a closed buffer should raise an exception."""
        buf = BoundedBuffer[int](maxsize=2)
        buf.close()
        with self.assertRaises(RuntimeError):
            buf.put(1)

    def test_multiple_producers(self):
        """Multiple producers can safely share the same buffer."""
        chunks = [list(range(i * 10, (i + 1) * 10)) for i in range(3)]
        buf = BoundedBuffer[int](maxsize=5)
        consumer = Consumer[int](buffer=buf)
        producers = [Producer[int](source=c, buffer=buf) for c in chunks]

        prod_threads = [threading.Thread(target=p.run) for p in producers]
        cons_thread = threading.Thread(target=consumer.run)

        for t in prod_threads:
            t.start()
        cons_thread.start()
        for t in prod_threads:
            t.join()
        buf.close()
        cons_thread.join()

        total_produced = sum(len(c) for c in chunks)
        self.assertEqual(len(consumer.dest), total_produced)
        self.assertEqual(sorted(consumer.dest), list(range(total_produced)))

    def test_multiple_consumers(self):
        """Multiple consumers share the work evenly and consume all data."""
        data = list(range(50))
        buf = BoundedBuffer[int](maxsize=5)
        consumer1 = Consumer[int](buffer=buf)
        consumer2 = Consumer[int](buffer=buf)
        producer = Producer[int](source=data, buffer=buf)

        t_prod = threading.Thread(target=producer.run)
        t_c1 = threading.Thread(target=consumer1.run)
        t_c2 = threading.Thread(target=consumer2.run)
        t_prod.start()
        t_c1.start()
        t_c2.start()
        t_prod.join()
        buf.close()
        t_c1.join()
        t_c2.join()

        total_consumed = len(consumer1.dest) + len(consumer2.dest)
        self.assertEqual(total_consumed, len(data))
        merged = sorted(consumer1.dest + consumer2.dest)
        self.assertEqual(merged, data)

    def test_fifo_order(self):
        """Consumers should receive items in the same order as produced."""
        data = list(range(100))
        buf = BoundedBuffer[int](maxsize=10)
        consumer = Consumer[int](buffer=buf)
        producer = Producer[int](source=data, buffer=buf)

        t_prod = threading.Thread(target=producer.run)
        t_cons = threading.Thread(target=consumer.run)
        t_prod.start()
        t_cons.start()
        t_prod.join()
        buf.close()
        t_cons.join()

        self.assertEqual(consumer.dest, data)

    def test_buffer_reuse(self):
        """Different buffer instances should not interfere with each other."""
        b1 = BoundedBuffer[int](maxsize=3)
        b2 = BoundedBuffer[int](maxsize=3)
        c1 = Consumer[int](buffer=b1)
        c2 = Consumer[int](buffer=b2)
        p1 = Producer[int](source=[1, 2, 3], buffer=b1)
        p2 = Producer[int](source=[10, 20, 30], buffer=b2)

        threads = [
            threading.Thread(target=p1.run),
            threading.Thread(target=p2.run),
            threading.Thread(target=c1.run),
            threading.Thread(target=c2.run),
        ]

        for t in threads:
            t.start()
        threads[0].join()
        b1.close()
        threads[1].join()
        b2.close()
        threads[2].join()
        threads[3].join()

        self.assertEqual(c1.dest, [1, 2, 3])
        self.assertEqual(c2.dest, [10, 20, 30])

    def test_performance_single_producer(self):
        """Benchmark: single producer and consumer throughput."""
        N = 10000
        buf = BoundedBuffer[int](maxsize=50)
        consumer = Consumer[int](buffer=buf)
        producer = Producer[int](source=list(range(N)), buffer=buf)

        start = time.time()
        t_prod = threading.Thread(target=producer.run)
        t_cons = threading.Thread(target=consumer.run)
        t_prod.start()
        t_cons.start()
        t_prod.join()
        buf.close()
        t_cons.join()
        end = time.time()

        duration = end - start
        throughput = N / duration
        print(f"\n[PERF] Single Producer: {N} items in {duration:.3f}s ({throughput:.1f} items/sec)")

        self.assertEqual(len(consumer.dest), N)
        self.assertLess(duration, 5.0, "Single producer too slow (>5s)")

    def test_performance_multi_producer(self):
        """Benchmark: multiple producers writing to one buffer."""
        producers_count = 4
        items_per_producer = 2500
        total = producers_count * items_per_producer

        buf = BoundedBuffer[int](maxsize=100)
        consumer = Consumer[int](buffer=buf)
        chunks = [
            list(range(i * items_per_producer, (i + 1) * items_per_producer))
            for i in range(producers_count)
        ]
        producers = [Producer[int](source=c, buffer=buf) for c in chunks]

        threads = [threading.Thread(target=p.run) for p in producers]
        cons_thread = threading.Thread(target=consumer.run)

        start = time.time()
        for t in threads:
            t.start()
        cons_thread.start()
        for t in threads:
            t.join()
        buf.close()
        cons_thread.join()
        end = time.time()

        duration = end - start
        throughput = total / duration
        print(f"[PERF] Multi-Producer: {total} items in {duration:.3f}s ({throughput:.1f} items/sec)")

        self.assertEqual(len(consumer.dest), total)
        self.assertLess(duration, 5.0, "Multi-producer too slow (>5s)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
