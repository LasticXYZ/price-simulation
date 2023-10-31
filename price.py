from linear import Linear

class CalculatePrice:
    def __init__(self):
        self.initial_bought_price = 1000
        self.new_buy_price = 1000

    def change_bought_price(self, new_bought_price):
        self.initial_bought_price = new_bought_price

    def update_renewal_price(self, config):
        cap_price = self.initial_bought_price * (1 + config.renewal_bump)
        self.initial_bought_price = min(cap_price, self.new_buy_price)

    @staticmethod
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

    @staticmethod
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
    
    def renew_price(self, sale_start, price, config, block_now):
        cap_price = self.initial_bought_price * (1 + config.renewal_bump)
        self.new_buy_price = min(cap_price, CalculatePrice.sale_price(sale_start, config, price, block_now))
        return self.new_buy_price

    def calculate_price(self, sale_start, config, price, block_now):
        if block_now < sale_start or block_now > (sale_start + config.region_length):
            raise ValueError("Invalid input: block_now must be greater than or equal to sale_start.")
        elif block_now < sale_start + config.interlude_length:
            return self.renew_price(sale_start, price, config, block_now)
        else:
            return self.sale_price(sale_start + config.interlude_length, config, price, block_now)