import unittest
from config import Config
from price import CalculatePrice


class TestCalculatePrice(unittest.TestCase):
    def setUp(self):
        self.config = Config(
            interlude_length=10,
            leadin_length=20,
            region_length=30,
            ideal_bulk_proportion=0.8,
            limit_cores_offered=None,
            renewal_bump=0.05,
        )
        self.calculate_price_obj = CalculatePrice(config=self.config)

    def test_update_renewal_price(self):
        initial_bought_price = 1000
        new_buy_price = 1200
        self.calculate_price_obj.initial_bought_price = initial_bought_price
        self.calculate_price_obj.new_buy_price = new_buy_price

        self.calculate_price_obj.update_renewal_price()

        price_cap = initial_bought_price * (1 + self.config.renewal_bump)
        expected_renewal_price = min(price_cap, new_buy_price)

        self.assertEqual(
            self.calculate_price_obj.initial_bought_price, expected_renewal_price
        )

    def test_rotate_sale(self):
        renewed_cores = 30
        sold_cores = 5
        self.calculate_price_obj.rotate_sale(renewed_cores, sold_cores)

        self.assertEqual(self.calculate_price_obj.price, 1000)

    def test_calculate_price_renewal(self):
        # Assuming we are in the renewal period (before interlude_length)
        region_start = 0
        block_now = 5

        calculated_price = self.calculate_price_obj.calculate_price(
            region_start, block_now
        )

        self.assertEqual(calculated_price, 1050)

    def test_calculate_price_sale(self):
        # Assuming we are in the sale period (after interlude_length)
        region_start = 15
        block_now = 25

        calculated_price = self.calculate_price_obj.calculate_price(
            region_start, block_now
        )

        self.assertEqual(calculated_price, 2000)


if __name__ == "__main__":
    unittest.main()
