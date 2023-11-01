from linear import Linear

class CalculatePrice:
    """
    This class is responsible for calculating the prices associated with sales over time.
    """
    def __init__(self, config):
        # price for which the cores were bought - important for renewal
        self.initial_bought_price = 1000
        # price for which the cores will be bought in the next sale
        self.new_buy_price = 1000
        # The latest price at which Bulk Coretime was purchased until surpassing the ideal number of cores were sold.
        self.sellout_price = None
        self.config = config
        self.price = 1000
        # The number of cores sold in the previous sale.
        self.cores_sold = 0

    def change_initial_price(self, new_initial_price):
        """
        Update the initial price of the core.

        :param new_initial_price: The new initial price to set.
        """
        self.price = new_initial_price

    def change_bought_price(self, new_bought_price):
        """
        Update the initial bought price of the core.

        :param new_bought_price: The new initial bought price to set.
        """
        self.initial_bought_price = new_bought_price

    def update_config(self, config):
        """
        Update the configuration object.

        :param config: The new configuration object to set.
        """
        self.config = config

    def update_renewal_price(self):
        """
        Update the renewal price based on the initial bought price and the new buy price.
        """
        cap_price = self.initial_bought_price * (1 + self.config.renewal_bump)
        self.initial_bought_price = min(cap_price, self.new_buy_price)

    def start_price_calculate(self, sold):
        """
        Calculate the starting price for the upcoming sale based on the number of cores sold.

        :param sold: The number of cores sold in the previous sale.
        """
        self.cores_sold = sold
        # Calculate the start price for the upcoming sale
        # Update price for new cycle
        offered = self.config.limit_cores_offered
        ideal = int(self.config.ideal_bulk_proportion * offered)
        if offered == 0:
            # No cores offered for sale - no purchase price.
            purchase_price = None
        elif sold >= ideal:
            # Sold more than the ideal amount. We should look for the last purchase price
            # before the sell-out. If there was no purchase at all, then we avoid having a
            # price here so that we make no alterations to it (since otherwise we would
            # increase it).
            purchase_price = self.sellout_price
        else:
            # Sold less than the ideal - we fall back to the regular price.
            purchase_price = self.price

        if purchase_price is not None:
            self.price = Linear.adapt_price(sold, ideal, offered) * purchase_price

    def __sale_price_calculate(self, region_start, block_now):
        """
        Calculate the sale price at a given block time.

        :param region_start: The starting block of the current region.
        :param block_now: The current block.
        :return: The calculated sale price.
        """
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

        # Update the sellout price if we have sold more than the ideal number of cores or if we have not yet set a sellout price.
        ideal = int(self.config.ideal_bulk_proportion * self.config.limit_cores_offered)
        if self.cores_sold <= ideal or self.sellout_price is None:
            self.sellout_price = self.price

        return sale_price
    
    def __renew_price(self, region_start, block_now):
        """
        Calculate the new buy price after renewal.

        :param region_start: The starting block of the current region.
        :param block_now: The current block.
        :return: The new buy price after renewal.
        """
        cap_price = self.initial_bought_price * (1 + self.config.renewal_bump)
        self.new_buy_price = min(cap_price, self.__sale_price_calculate(region_start, block_now))
        return self.new_buy_price

    def calculate_price(self, region_start, block_now):
        """
        Calculate the price at a specific block, taking into account whether it is in the renewal period or sale period.

        :param region_start: The starting block of the current region.
        :param block_now: The current block.
        :return: The calculated price.
        """
        if not region_start <= block_now <= (region_start + self.config.region_length):
            raise ValueError("Invalid input: block_now must be greater than or equal to region_start.")
        elif block_now < region_start + self.config.interlude_length:
            return self.__renew_price(region_start, block_now)
        else:
            return self.__sale_price_calculate(region_start + self.config.interlude_length, block_now)