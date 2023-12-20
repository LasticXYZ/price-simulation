import unittest
from config import Config
from price import CalculatePrice


class TestCalculatePrice(unittest.TestCase):
    def setUp(self):
        self.config = Config(
            interlude_length=7 * 5,
            leadin_length=7 * 5,
            region_length=28 * 5,
            ideal_bulk_proportion=0.6,
            limit_cores_offered=50,
            renewal_bump=0.05,
        )
        self.calculate_price_obj = CalculatePrice(config=self.config)

    def test_calculate_price_renewal_period(self):
        # Test when block_now is within the renewal period

        # Set up
        region_start = 0
        block_now = region_start + self.config.interlude_length // 2

        # Call the function to test
        calculated_price = self.calculate_price_obj.calculate_price(
            region_start, block_now
        )

        # Validate the result
        expected_price = self.calculate_price_obj._CalculatePrice__renew_price(
            region_start, block_now
        )
        self.assertAlmostEqual(calculated_price, expected_price, delta=0.001)

    def test_calculate_price_sale_period(self):
        # Test when block_now is within the sale period

        region_start = 0
        block_now = (
            region_start + self.config.interlude_length + self.config.leadin_length // 2
        )

        # Call the function
        calculated_price = self.calculate_price_obj.calculate_price(
            region_start, block_now
        )

        # Validate the expected price
        expected_price = self.calculate_price_obj._CalculatePrice__sale_price_calculate(
            region_start + self.config.interlude_length, block_now
        )
        self.assertAlmostEqual(calculated_price, expected_price, delta=0.001)

    def test_calculate_price_outside_periods(self):
        # Test when block_now is outside both renewal and sale periods

        region_start = 0
        block_now = region_start - 1

        # Call the function
        with self.assertRaises(ValueError):
            self.calculate_price_obj.calculate_price(region_start, block_now)

        # Set up after sale period
        block_now = region_start + self.config.region_length + 1

        # Call the function to test
        with self.assertRaises(ValueError):
            self.calculate_price_obj.calculate_price(region_start, block_now)


if __name__ == "__main__":
    unittest.main()
