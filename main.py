from linear import Linear
from config import Config
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


def start_price_calculate(old_price, config, sold):
    # Calculate the start price for the upcoming sale
    offered = config.limit_cores_offered
    ideal = int(config.ideal_bulk_proportion * offered)
    if offered == 0:
        # No cores offered for sale - no purchase price.
        purchase_price = None
    # elif sold >= ideal:
    #     # Sold more than the ideal amount. We should look for the last purchase price
    #     # before the sell-out. If there was no purchase at all, then we avoid having a
    #     # price here so that we make no alterations to it (since otherwise we would
    #     # increase it).
    #     purchase_price = old_sale.sellout_price
    else:
        # Sold less than the ideal - we fall back to the regular price.
        purchase_price = old_price

    if purchase_price is None:
        price = old_price
    else:
        price = Linear.adapt_price(sold, ideal, offered) * purchase_price

    return price

def sale_price(sale_start, config, price, block_now):
    # Calculate the sale price at a given block time

    leadin_length = config.leadin_length
    
    # Ensure the values are positive and of correct type
    sale_start, leadin_length, price, block_now = map(int, [sale_start, leadin_length, price, block_now])
    if sale_start < 0 or leadin_length <= 0 or price < 0 or block_now < 0:
        raise ValueError("Invalid input: sale_start, leadin_length, price, and block_now must be non-negative. leadin_length must be positive.")
    
    # Calculate num
    num = max(block_now - sale_start, 0)
    num = min(num, leadin_length)
    
    # Calculate through
    through = num / leadin_length
    
    # Calculate the lead-in factor (LF). You need to define how LF is calculated based on through.
    # For example, if LF is a linear function of through, you have:
    LF = Linear.leadin_factor_at(through)
    
    # Calculate sale price
    sale_price = LF * price

    return sale_price

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
        
        sale_prices = [sale_price(region_start, config, price, block_now) for block_now in block_times]
        plot_sale_price(ax, block_times, sale_prices, region_start, config.leadin_length, config.region_length, f'Region {region_i+1}')

        # Recalculate the price at the end of each region
        price = start_price_calculate(price, config, sold_cores_in_each_sale)

    ax.set_xlabel('Block Time')
    ax.set_ylabel('Sale Price')
    ax.set_title('Sale Price over Time')
    ax.legend()
    st.pyplot(fig)

def plot_sale_price(ax, block_times, sale_prices, region_start, leadin_length, region_length, label):
    ax.plot(block_times, sale_prices, label=label)
    ax.axvline(x=region_start, color='r', linestyle='--')
    ax.axvline(x=region_start + leadin_length, color='g', linestyle='--')
    ax.axvline(x=region_start + region_length, color='b', linestyle='--')

if __name__ == "__main__":
    main()