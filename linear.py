class Linear:
    @staticmethod
    def leadin_factor_at(when):
        return 2 - when

    @staticmethod
    def adapt_price(sold, target, limit):
        if sold <= target:
            return sold / target
        else:
            return 1 + (sold - target) / (limit - target)
