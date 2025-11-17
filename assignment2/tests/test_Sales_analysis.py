import unittest
from assignment2.sales_analysis import (
    read_sales, total_revenue, revenue_by_region, revenue_by_category,
    top_n_products_by_revenue, monthly_revenue_trend,
    average_discount_by_category, highest_order_value
)

CSV_PATH = "assignment2/data/sales.csv"

class TestSalesAnalysis(unittest.TestCase):
    def setUp(self):
        self.data = read_sales(CSV_PATH)

    def test_total_revenue(self):
        total = total_revenue(self.data)
        self.assertTrue(total > 0)

    def test_revenue_by_region(self):
        regions = revenue_by_region(self.data)
        self.assertIn("North", regions)
        self.assertTrue(all(v > 0 for v in regions.values()))

    def test_revenue_by_category(self):
        cats = revenue_by_category(self.data)
        self.assertIn("Electronics", cats)
        self.assertTrue(sum(cats.values()) > 0)

    def test_top_products(self):
        top = top_n_products_by_revenue(self.data, 3)
        self.assertEqual(len(top), 3)
        self.assertTrue(top[0][1] >= top[1][1])

    def test_monthly_trend(self):
        trend = monthly_revenue_trend(self.data)
        self.assertTrue("2024-01" in trend)

    def test_avg_discount(self):
        avg = average_discount_by_category(self.data)
        self.assertTrue(all(0 <= v <= 1 for v in avg.values()))

    def test_highest_order(self):
        oid, val = highest_order_value(self.data)
        self.assertTrue(oid.startswith("O"))
        self.assertTrue(val > 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
