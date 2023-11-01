from linear import Linear

class CalculatePrice:
    def __init__(self, config):
        self.initial_bought_price = 1000
        self.new_buy_price = 1000
        self.sellout_price = 1000
        self.config = config
        self.price = 1000

    def change_initial_price(self, new_initial_price):
        self.price = new_initial_price

    def change_bought_price(self, new_bought_price):
        self.initial_bought_price = new_bought_price

    def update_config(self, config):
        self.config = config

    def update_renewal_price(self):
        cap_price = self.initial_bought_price * (1 + self.config.renewal_bump)
        self.initial_bought_price = min(cap_price, self.new_buy_price)

    def start_price_calculate(self, sold):
        # Calculate the start price for the upcoming sale
        # Update price for new cycle
        offered = self.config.limit_cores_offered
        ideal = int(self.config.ideal_bulk_proportion * offered)
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
            purchase_price = self.price

        if purchase_price is not None:
            self.price = Linear.adapt_price(sold, ideal, offered) * purchase_price

    def sale_price_calculate(self, region_start, block_now):
        # Calculate the sale price at a given block time
        leadin_length = self.config.leadin_length
        
        # Calculate num
        num = max(block_now - region_start, 0)
        num = min(num, leadin_length)
        
        # Calculate through
        through = num / leadin_length
        
        # Calculate the lead-in factor (LF). You need to define how LF is calculated based on through.
        # For example, if LF is a linear function of through, you have:
        LF = Linear.leadin_factor_at(through)
        
        # Calculate sale price
        sale_price = LF * self.price

        return sale_price
    
    def renew_price(self, region_start, block_now):
        cap_price = self.initial_bought_price * (1 + self.config.renewal_bump)
        self.new_buy_price = min(cap_price, self.sale_price_calculate(region_start, block_now))
        return self.new_buy_price

    def calculate_price(self, region_start, block_now):
        if not region_start <= block_now <= (region_start + self.config.region_length):
            raise ValueError("Invalid input: block_now must be greater than or equal to region_start.")
        elif block_now < region_start + self.config.interlude_length:
            return self.renew_price(region_start, block_now)
        else:
            return self.sale_price_calculate(region_start + self.config.interlude_length, block_now)