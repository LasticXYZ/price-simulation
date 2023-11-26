from config import Config
from price import CalculatePrice
from streamlitapp import StreamlitApp

BLOCKS_PER_DAY = 5
SALE_START = 0

def main():
    # Initial configuration
    config = Config(
        interlude_length=7 * BLOCKS_PER_DAY,
        leadin_length=7 * BLOCKS_PER_DAY,
        region_length=28 * BLOCKS_PER_DAY,
        ideal_bulk_proportion=0.6,
        limit_cores_offered=50,
        renewal_bump=0.05,
    )
    price_calculator = CalculatePrice(config)
    app = StreamlitApp(config, price_calculator)

    # Plotting and displaying results
    app.run()

if __name__ == "__main__":
    main()