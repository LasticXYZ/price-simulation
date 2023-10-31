from linear import Linear
from config import Config
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


def start_price_calculate(old_sale, config):
    # Calculate the start price for the upcoming sale
    offered = old_sale.cores_offered
    ideal = old_sale.ideal_cores_sold
    sold = old_sale.cores_sold
    if offered == 0:
        # No cores offered for sale - no purchase price.
        purchase_price = None
    elif sold >= ideal:
        # Sold more than the ideal amount. We should look for the last purchase price
        # before the sell-out. If there was no purchase at all, then we avoid having a
        # price here so that we make no alterations to it (since otherwise we would
        # increase it).
        purchase_price = old_sale.sellout_price
    else:
        # Sold less than the ideal - we fall back to the regular price.
        purchase_price = old_sale.price

    if purchase_price is None:
        price = old_sale.price
    else:
        price = Linear.adapt_price(sold, ideal, offered) * purchase_price

    return price

def rotate_sale(old_sale, config, block_now):

    # Calculate the start price for the upcoming sale
    start_price_calculate(old_sale, config)

    cores_offered = config.limit_cores_offered
    sale_start = max(block_now + config.interlude_length, 0)
    leadin_length = config.leadin_length
    ideal_cores_sold = int(config.ideal_bulk_proportion * cores_offered)
    
    
    print("ideal_cores_sold", ideal_cores_sold)
    print("cores_offered", cores_offered)
    print("sale_start", sale_start)
    print("leadin_length", leadin_length)

def sale_price(sale_start, config, price, block_now):
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

if __name__ == "__main__":
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

    # Create input fields and collect updated values
    updated_values = {}
    for attribute_name in dir(config):
        if not attribute_name.startswith("__") and not callable(getattr(config, attribute_name)):
            value = st.number_input(attribute_name, value=getattr(config, attribute_name))
            updated_values[attribute_name] = value

    # Update the configuration based on user input
    config.update_config(updated_values)

    st.write("Updated Config:", config)


    # Create a slider for the sale start and price
    sale_start = st.slider('Sale Start', min_value=0, max_value=100, value=10, step=1)
    price = st.slider('Price', min_value=0, max_value=2000, value=1000, step=10)

    block_times = np.linspace(sale_start, sale_start + config.region_length, 100)
    sale_prices = [sale_price(sale_start, config, price, block_now) for block_now in block_times]

    fig, ax = plt.subplots()
    ax.plot(block_times, sale_prices, 'bo')
    ax.set_xlabel('Block Time')
    ax.set_ylabel('Sale Price')
    ax.set_title('Sale Price over Time')
    ax.axvline(x=sale_start, color='r', linestyle='--', label='Sale Start')
    ax.axvline(x=sale_start + config.leadin_length, color='g', linestyle='--', label='Sale End')
    ax.legend()

    st.pyplot(fig)




