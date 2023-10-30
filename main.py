from linear import Linear
from config import Config
import numpy as np
import matplotlib.pyplot as plt

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
    config = Config(
        advance_notice=1,
        interlude_length=50,
        leadin_length=25,
        region_length=100,
        ideal_bulk_proportion=0.6,
        limit_cores_offered=None,
        renewal_bump=0.01,
        contribution_timeout=1000
    )

    

    sale_start = 10
    price = 100

    block_times = np.linspace(sale_start, sale_start + config.leadin_length + 10, 100)
    sale_prices = [sale_price(sale_start, config, price, block_now) for block_now in block_times]

    plt.plot(block_times, sale_prices, 'bo')
    plt.xlabel('Block Time')
    plt.ylabel('Sale Price')
    plt.title('Sale Price over Time')
    plt.axvline(x=sale_start, color='r', linestyle='--', label='Sale Start')
    plt.axvline(x=sale_start + config.leadin_length, color='g', linestyle='--', label='Sale End')
    plt.legend()
    plt.show()




