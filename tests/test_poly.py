import unittest
from poly import Linear, Exponential


class TestLinearNoPanic(unittest.TestCase):
    def test_linear_no_panic(self):
        for limit in range(10):
            for target in range(1, 10):
                for sold in range(limit + 1):
                    price = Linear.adapt_price(sold, target, limit)

                    if sold > target:
                        self.assertTrue(price > 1)
                    else:
                        self.assertTrue(price <= 1)


class TestExponentialNoPanic(unittest.TestCase):
    def test_exponential_no_panic(self):
        for limit in range(10):
            for target in range(1, 10):
                for sold in range(limit + 1):
                    price = Exponential.adapt_price(sold, target, limit)

                    if sold > target:
                        self.assertTrue(price > 1)
                    else:
                        self.assertTrue(price <= 1)


if __name__ == "__main__":
    unittest.main()
