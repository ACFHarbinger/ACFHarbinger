import unittest
from src.rank_calculator import exponential_cdf, log_normal_cdf, calculate_rank

class TestRankCalculator(unittest.TestCase):
    def test_exponential_cdf(self):
        self.assertEqual(exponential_cdf(0), 0)
        self.assertGreater(exponential_cdf(1), 0)
        self.assertLessEqual(exponential_cdf(10), 1.0)

    def test_log_normal_cdf(self):
        self.assertEqual(log_normal_cdf(0), 0.0)
        self.assertEqual(log_normal_cdf(-1), 0.0)
        self.assertEqual(log_normal_cdf(1), 0.5)

    def test_calculate_rank_tiers(self):
        # High stats should result in S or A+
        level_top, pct_top = calculate_rank(10000, 500, 200, 50, 1000, 500)
        self.assertIn(level_top, ["S", "A+"])
        self.assertLess(pct_top, 15.0)

        # Baseline stats
        level_base, pct_base = calculate_rank(100, 5, 2, 0, 5, 2)
        self.assertIn(level_base, ["B", "B-", "C+", "C"])

if __name__ == "__main__":
    unittest.main()
