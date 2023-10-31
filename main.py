from config import Config
from price import CalculatePrice
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def get_config_input(config):
    # Create input fields and collect updated values
    updated_values = {}
    for attribute_name in dir(config):
        if not attribute_name.startswith("__") and not callable(getattr(config, attribute_name)):
            value = st.number_input(attribute_name, value=getattr(config, attribute_name))
            updated_values[attribute_name] = value
    return updated_values

def get_slider_input():
    # Create a slider for the sale start and price
    sale_start = st.slider('Sale Start', min_value=0, max_value=100, value=10, step=1)
    price = st.slider('Starting Price', min_value=0, max_value=2000, value=1000, step=10)
    observe_blocks = st.slider('Observe Blocks', min_value=100, max_value=1000, value=200, step=10)
    sold_cores_in_each_sale = st.slider('Cores sold in each sale', min_value=0, max_value=50, value=10, step=10)
    return sale_start, price, observe_blocks, sold_cores_in_each_sale

def plot_sale_price(ax, block_times, sale_prices, region_start, leadin_length, region_length, label):
    ax.plot(block_times, sale_prices, label=label)
    ax.axvline(x=region_start, color='r', linestyle='--')
    ax.axvline(x=region_start + leadin_length, color='g', linestyle='--')
    ax.axvline(x=region_start + region_length, color='b', linestyle='--')

def main():
    st.title('Sale Price over Time')

    # Initial configuration
    config = Config(
        interlude_length=50,
        leadin_length=25,
        region_length=100,
        ideal_bulk_proportion=0.6,
        limit_cores_offered=50,
        renewal_bump=0.02,
    )

    # Update the configuration based on user input
    updated_values = get_config_input(config)
    config.update_config(updated_values)

    sale_start, initial_price, observe_blocks, sold_cores_in_each_sale = get_slider_input()

    region_nb = int(observe_blocks / config.region_length)
    
    fig, ax = plt.subplots()
    price = initial_price
    for region_i in range(region_nb):
        region_start = sale_start + region_i * config.region_length
        block_times = np.linspace(region_start, region_start + config.region_length, 100)
        
        sale_prices = [CalculatePrice.sale_price(region_start, config, price, block_now) for block_now in block_times]
        plot_sale_price(ax, block_times, sale_prices, region_start, config.leadin_length, config.region_length, f'Region {region_i+1}')

        # Recalculate the price at the end of each region
        price = CalculatePrice.start_price_calculate(price, config, sold_cores_in_each_sale)

    ax.set_xlabel('Block Time')
    ax.set_ylabel('Sale Price')
    ax.set_title('Sale Price over Time')
    ax.legend()
    st.pyplot(fig)

if __name__ == "__main__":
    main()