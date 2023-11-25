class Linear:
    @staticmethod
    def leadin_factor_at(when, factor = 1):
        # Factor represents the slope of the linear function
        # Factor is not a parameter that is originally used in the `broker pallet code`.
        return (2 - when) * factor

    @staticmethod
    def adapt_price(sold, target, limit):
        if sold <= target:
            return max(sold, 1) / target
        else:
            return 1 + (sold - target) / (limit - target)


class Exponential:
    @staticmethod
    def leadin_factor_at(when, factor: int = 1):
        # Exponential decay model for the lead-in factor
        # Factor is not a parameter that is originally used in the `broker pallet code`.
        return pow(2 - when, factor)

    @staticmethod
    def adapt_price(sold, target, limit):
        # Exponential price adaptation based on the sold quantity
        if sold <= target:
            return pow(2, -sold/target)  # Decreases exponentially as sold approaches target
        else:
            # Increases exponentially as sold exceeds target, up to the limit
            excess_ratio = (sold - target) / (limit - target)
            return 1 + pow(2, excess_ratio)
