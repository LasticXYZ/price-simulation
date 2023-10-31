from dataclasses import dataclass

@dataclass
class Config:
    def __init__(self, interlude_length, leadin_length, region_length, ideal_bulk_proportion, limit_cores_offered, renewal_bump):
        # The length in blocks of the Interlude Period for forthcoming sales.
        self.interlude_length = interlude_length
        # The length in blocks of the Leadin Period for forthcoming sales.
        self.leadin_length = leadin_length
        # The length in blocks of the Region Period for forthcoming sales.
        self.region_length = region_length
        # The proportion of cores available for sale which should be sold in order for the price to remain the same in the next sale.
        self.ideal_bulk_proportion = ideal_bulk_proportion
        # An artificial limit to the number of cores which are allowed to be sold. If `Some` thenno more cores will be sold than this.
        self.limit_cores_offered = limit_cores_offered
        # The amount by which the renewal price increases each sale period.
        self.renewal_bump = renewal_bump

    def update_config(self, updated_values):
        for key, value in updated_values.items():
            if hasattr(self, key):
                setattr(self, key, value)