from linear import Linear

class CalculatePrice:
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
