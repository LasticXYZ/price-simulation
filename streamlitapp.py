import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from helpercss import create_tooltip

BLOCKS_PER_DAY = 5
SALE_START = 0

class StreamlitApp:
    def __init__(self, config, price_calculator):
        """
        Initialize the Streamlit app with configuration and price calculator.
        """
        self.config = config
        self.price_calculator = price_calculator

    def get_config_input(self):
        """
        Create input fields for configuration and collect updated values.
        """
        help_texts = self._get_help_texts()

        # Create input fields and collect updated values
        with st.expander("Configuration values"):
            updated_values = {}
            for attribute_name in dir(self.config):
                if not attribute_name.startswith("__") and not callable(getattr(self.config, attribute_name)):
                    help_text = help_texts.get(attribute_name, "")  # Get help text or default to empty string
                    value = st.number_input(attribute_name, value=getattr(self.config, attribute_name), help=help_text)
                    updated_values[attribute_name] = value
        return updated_values

    def _get_help_texts(self):
        """
        Returns a dictionary of help texts for each configuration attribute.
        """
        return {
            "interlude_length": "Length in blocks of the Interlude Period for forthcoming sales.",
            "leadin_length": "Length in blocks of the Leadin Period for forthcoming sales.",
            "region_length": "Length in blocks of the Region Period for forthcoming sales.",
            "ideal_bulk_proportion": "Proportion of cores available for sale to maintain stable price.",
            "limit_cores_offered": "Artificial limit to the number of cores allowed to be sold.",
            "renewal_bump": "Amount by which the renewal price increases each sale period."
        }

    def get_slider_input(self):
        # Create a slider for the sale start and price

        observe_time = st.slider('X-AXIS - Observing time', min_value= 1, max_value=20, value=2, step=1, help='Number of regions to observe: Nb.of regions (28 day chunks)')
        observe_blocks = observe_time * self.config.region_length

        initial_bought_price = st.slider('Y-AXIS - Start Price of the Core You Bought', min_value=0, max_value=10000, value=1000, step=10)
        self.price_calculator.change_bought_price(initial_bought_price)
        price = st.slider('Y-AXIS Starting Price', min_value=0, max_value=10000, value=1000, step=10)
        self.price_calculator.change_initial_price(price)

        with st.expander("Factor curve"):
            st.write("Change the lead-in factor (LF) curve - To exponential or linear")

            linear = st.toggle('-', value=True, help='Toggle between exponential and linear')
            if linear:
                linear_text = 'Current value: Linear'
            else:
                linear_text = 'Current value: Exponential'
            st.write(linear_text)

            self.price_calculator.change_linear(linear)
            factor_value = st.slider('Factor Value', min_value=1, max_value=10, value=1, step=1, help='Factor value for the lead-in factor curve')
            self.price_calculator.change_factor(factor_value)
        
            st.write(self.price_calculator.get_factor(), self.price_calculator.get_linear())

        st.header("Cores Renewed and Sold in Each Sale")
        renewed_cores_in_each_sale = st.slider('Cores renewed in each sale', min_value=0, max_value=self.config.limit_cores_offered, value=10, step=1)
        if self.config.limit_cores_offered - renewed_cores_in_each_sale > 0:
            sold_cores_in_each_sale = st.slider('Cores sold in each sale', min_value=0, max_value=self.config.limit_cores_offered - renewed_cores_in_each_sale, value=0, step=1)
        else:
            sold_cores_in_each_sale = 0

        st.markdown("### Adjustment for each region length (28 days)")
        monthly_renewals = {}
        monthly_sales = {}
        for month in range(1, observe_time + 1):
            with st.expander(f"Region {month} Adjustments"):
                renewed_cores = st.slider(f'Cores renewed in Month {month}', min_value=0, max_value=self.config.limit_cores_offered, value=10, step=1)
                if self.config.limit_cores_offered - renewed_cores > 0:
                    sold_cores = st.slider(f'Cores sold in Month {month}', min_value=0, max_value=self.config.limit_cores_offered - renewed_cores, value=0, step=1)
                else:
                    sold_cores = 0
                monthly_renewals[month] = renewed_cores
                monthly_sales[month] = sold_cores
            st.write("Region nb. ", month, ": Renewals ", renewed_cores, ", Sold ", sold_cores)

        return observe_blocks, renewed_cores_in_each_sale, sold_cores_in_each_sale

    def plot_sale_price(self, ax, block_times, sale_prices, region_start, label):
        ax.plot(block_times, sale_prices, label=label)
        ax.axvline(x=region_start, color='r', linestyle='--')
        ax.axvline(x=region_start + self.config.interlude_length, color='y', linestyle='--')
        ax.axvline(x=region_start + self.config.interlude_length + self.config.leadin_length, color='g', linestyle='--')
        ax.axvline(x=region_start + self.config.region_length, color='b', linestyle='--')

    def run(self):
        """
        Run the Streamlit application.
        """
        st.title('Sale Price over Time')
        
        # Sidebar for Configuration Input
        with st.sidebar:
            st.header("Configuration Settings")
            # Update the configuration based on user input
            updated_values = self.get_config_input()
            self.config.update_config(updated_values)
            self.price_calculator.update_config(self.config)

            st.header("Sale Settings")
            observe_blocks, renewed_cores_in_each_sale, sold_cores_in_each_sale = self.get_slider_input()

        st.markdown(create_tooltip("Red-Yellow: INTERLUDE PERIOD", "The area between the red and yellow section represents the INTERLUDE Period, this is the time when accounts who bought their cores in previous blocks can renew them."), unsafe_allow_html=True)
        st.markdown(create_tooltip("Yellow-Green: LEADIN PERIOD", "The area between the yellow and green section represents the LEADIN Period, this is the time when new sales occur."), unsafe_allow_html=True)

        region_nb = int(observe_blocks / self.config.region_length)

        fig, ax = plt.subplots()
        for region_i in range(region_nb):
            region_start = SALE_START + region_i * self.config.region_length
            block_times = np.linspace(region_start, region_start + self.config.region_length, self.config.region_length)
            
            sale_prices = [self.price_calculator.calculate_price(region_start, block_now) for block_now in block_times]
            self.plot_sale_price(ax, block_times, sale_prices, region_start, f'Region {region_i+1}')

            # Recalculate the price of renewal of the core
            self.price_calculator.update_renewal_price()
            # Recalculate the price at the end of each region
            self.price_calculator.start_price_calculate(renewed_cores_in_each_sale, sold_cores_in_each_sale)

        ax.set_xlabel('Block Time')
        ax.set_ylabel('Sale Price')
        ax.set_title('Sale Price over Time')
        ax.legend()
        st.pyplot(fig)
