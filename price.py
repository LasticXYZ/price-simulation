from poly import Linear, Exponential

class CalculatePrice:
    """
    This class is responsible for calculating the prices associated with sales over time.

    """
    def __init__(self, config):
        # The leadin factor is either linear or exponential depending on the value of self.linear
        self.linear = False
        self.factor = 1
        # price for which the cores were bought - important for renewal
        self.initial_bought_price = 1000
        # price for which the cores will be bought in the next sale
        self.new_buy_price = 1000
        # The latest price at which Bulk Coretime was purchased until surpassing the ideal number of cores were sold.
        # we will assume that the last purchase was done at the lowest price of the sale.
        self.sellout_price = None
        self.config = config
        self.price = 1000
        # The number of cores sold in the previous sale.
        self.cores_sold_in_renewal = 40
        self.cores_sold_in_sale = 6
        self.cores_sold = self.cores_sold_in_renewal + self.cores_sold_in_sale

    def get_factor(self):
        """
        Get the factor of the exponential or linear function.
        """
        return self.factor
    
    def get_linear(self):
        """
        Get the factor of the exponential or linear function.
        """
        return self.linear

    def change_linear(self, linear):
        """
        Update the linear factor.

        :param linear: The new linear factor to set.
        """
        self.linear = linear

    def change_factor(self, factor):
        """
        Update the factor. Of the exponential or linear function.

        :param factor: The new factor to set.
        """
        self.factor = factor

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
        Checkout imitated code at: https://github.com/paritytech/polkadot-sdk/blob/2610450a18e64079abfe98f0a5b57069bbb61009/substrate/frame/broker/src/dispatchable_impls.rs#L155C7-L157
        """
        price_cap = self.initial_bought_price * (1 + self.config.renewal_bump)
        self.initial_bought_price = min(price_cap, self.new_buy_price)

    def rotate_sale(self, renewed_cores, sold_cores):
        """
        Calculate the starting price for the upcoming sale based on the number of cores sold.
        Imitates function `rotate_sale`: https://github.com/paritytech/polkadot-sdk/blob/4298bc608fa8e5d8b8fb1ca0c1028613d82bc99b/substrate/frame/broker/src/tick_impls.rs#L138

        :param sold: The number of cores sold in the previous sale.
        """
        self.cores_sold_in_renewal = renewed_cores
        self.cores_sold_in_sale = sold_cores
        self.cores_sold = self.cores_sold_in_renewal + self.cores_sold_in_sale
        # Calculate the start price for the upcoming sale
        # Update price for new cycle
        offered = self.config.limit_cores_offered
        ideal = int(self.config.ideal_bulk_proportion * offered)
        if offered == 0:
            # No cores offered for sale - no purchase price.
            purchase_price = None
        elif self.cores_sold >= ideal:
            # Sold more than the ideal amount. We should look for the last purchase price
            # before the sell-out. If there was no purchase at all, then we avoid having a
            # price here so that we make no alterations to it (since otherwise we would
            # increase it).
            purchase_price = self.sellout_price
        else:
            # Sold less than the ideal - we fall back to the regular price.
            purchase_price = self.price

        if purchase_price is not None:
            self.price = Linear.adapt_price(self.cores_sold, ideal, offered) * purchase_price

    def __sale_price_calculate(self, region_start, block_now):
        """
        Calculate the sale price at a given block time.
        Function imitates `do_purchase`: https://github.com/paritytech/polkadot-sdk/blob/2610450a18e64079abfe98f0a5b57069bbb61009/substrate/frame/broker/src/dispatchable_impls.rs#L97
        and `sale_price`: https://github.com/paritytech/polkadot-sdk/blob/4298bc608fa8e5d8b8fb1ca0c1028613d82bc99b/substrate/frame/broker/src/utility_impls.rs#L63
        
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
        # Choose linear or exponential.
        if self.linear == True:
            LF = Linear.leadin_factor_at(through, factor=self.factor)
        else:
            LF = Exponential.leadin_factor_at(through, factor=self.factor)
        
        # Calculate sale price
        sale_price = LF * self.price

        # Update the sellout price
        self.__sellout_price_update()

        return sale_price
    
    def __sellout_price_update(self):
        """
        Update the sellout price until we have sold less than the ideal number
        of cores or if we have not yet set a sellout price.
        We assume that the cores that were sold in the sell period were sold at the lowest price of the sale.

        :param region_start: The starting block of the current region.
        :param block_now: The current block.
        :return: The calculated sellout price.
        """
        ideal = int(self.config.ideal_bulk_proportion * self.config.limit_cores_offered)
        if (self.cores_sold_in_renewal <= ideal and self.cores_sold_in_sale > 0) or self.sellout_price is None:
            self.sellout_price = self.price


    def __renew_price(self, region_start, block_now):
        """
        Calculate the new buy price after renewal.
        Function imitates `do_renew`: https://github.com/paritytech/polkadot-sdk/blob/2610450a18e64079abfe98f0a5b57069bbb61009/substrate/frame/broker/src/dispatchable_impls.rs#L125

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