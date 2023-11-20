from config import Config
from price import CalculatePrice
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

BLOCKS_PER_DAY = 4
SALE_START = 0

def get_config_input(config):
    # Create input fields and collect updated values
    with st.expander("Configuration values"):
        st.write("""
                Configuration values:
                - interlude_length: The length in blocks of the Interlude Period for forthcoming sales.
                - leadin_length: The length in blocks of the Leadin Period for forthcoming sales.
                - region_length: The length in blocks of the Region Period for forthcoming sales.
                - ideal_bulk_proportion: The proportion of cores available for sale which should be sold in order for the price to remain the same in the next sale.
                - limit_cores_offered: An artificial limit to the number of cores which are allowed to be sold. If `Some` thenno more cores will be sold than this.
                - renewal_bump: The amount by which the renewal price increases each sale period.
                """)
        updated_values = {}
        for attribute_name in dir(config):
            if not attribute_name.startswith("__") and not callable(getattr(config, attribute_name)):
                value = st.number_input(attribute_name, value=getattr(config, attribute_name))
                updated_values[attribute_name] = value
    return updated_values

def get_slider_input(config, price_calculator):
    # Create a slider for the sale start and price
    initial_bought_price = st.slider('Start Price of the Core You Bought', min_value=0, max_value=2000, value=1000, step=10)
    price_calculator.change_bought_price(initial_bought_price)
    price = st.slider('Starting Price', min_value=0, max_value=2000, value=1000, step=10)
    price_calculator.change_initial_price(price)

    observe_blocks = st.slider('Observe Blocks', min_value=config.region_length, max_value=20 * config.region_length, value=config.region_length * 2, step=config.region_length)
    renewed_cores_in_each_sale = st.slider('Cores renewed in each sale', min_value=0, max_value=config.limit_cores_offered, value=10, step=1)
    sold_cores_in_each_sale = st.slider('Cores sold in each sale', min_value=0, max_value=config.limit_cores_offered - renewed_cores_in_each_sale, value=2, step=1)
    return observe_blocks, renewed_cores_in_each_sale, sold_cores_in_each_sale

def plot_sale_price(ax, block_times, sale_prices, region_start, config, label):
    ax.plot(block_times, sale_prices, label=label)
    ax.axvline(x=region_start, color='r', linestyle='--')
    ax.axvline(x=region_start + config.interlude_length, color='y', linestyle='--')
    ax.axvline(x=region_start + config.interlude_length + config.leadin_length, color='g', linestyle='--')
    ax.axvline(x=region_start + config.region_length, color='b', linestyle='--')

def main():
    st.title('Sale Price over Time')

    # Initial configuration
    config = Config(
        interlude_length=7 * BLOCKS_PER_DAY,
        leadin_length=7 * BLOCKS_PER_DAY,
        region_length=28 * BLOCKS_PER_DAY,
        ideal_bulk_proportion=0.6,
        limit_cores_offered=50,
        renewal_bump=0.05,
    )

    price_calculator = CalculatePrice(config, linear=True)

    # Update the configuration based on user input
    updated_values = get_config_input(config)
    config.update_config(updated_values)
    price_calculator.update_config(config)

    observe_blocks, renewed_cores_in_each_sale, sold_cores_in_each_sale = get_slider_input(config, price_calculator)

    region_nb = int(observe_blocks / config.region_length)
    
    fig, ax = plt.subplots()
    for region_i in range(region_nb):
        region_start = SALE_START + region_i * config.region_length
        block_times = np.linspace(region_start, region_start + config.region_length, config.region_length)
        
        sale_prices = [price_calculator.calculate_price(region_start, block_now) for block_now in block_times]
        plot_sale_price(ax, block_times, sale_prices, region_start, config, f'Region {region_i+1}')

        # Recalculate the price of renewal of the core
        price_calculator.update_renewal_price()
        # Recalculate the price at the end of each region
        price_calculator.start_price_calculate(renewed_cores_in_each_sale, sold_cores_in_each_sale)

    ax.set_xlabel('Block Time')
    ax.set_ylabel('Sale Price')
    ax.set_title('Sale Price over Time')
    ax.legend()
    st.pyplot(fig)

if __name__ == "__main__":
    main()