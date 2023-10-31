# Core-Time Sale Price Calculator

This project provides a tool to calculate and visualize the sale price of Coretime  over blocktime based on various parameters. It is implemented in Python and utilizes the Streamlit library for creating an interactive web application.

## Features

- Interactive sliders to adjust sale parameters.
- Real-time graph visualization of sale prices over time.
- Configurable region lengths and lead-in lengths for sale price calculation.
- Adaptation of sale price based on the number of cores sold.

## Getting Started

### Prerequisites

- Python 3.x
- Pip (Python package installer)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/lastic_xyz/sale-price-calculator.git
   cd sale-price-calculator
   ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

    or install the main requirements with:
    ```sh
    pip install numpy matplotlib streamlit
    ```

3. Run the Streamlit application:
   ```sh
   streamlit run main.py
   ```

### Usage

- Adjust the parameters using the sliders on the left panel.
- Observe the real-time changes in the sale price graph.
- The sale price is recalculated at the end of each region based on the number of cores sold.

## Configuration

You can configure various parameters of the sale price calculation in the `config.py` file. Please refer to the comments in the file for explanations of each parameter.

## Contributing

Contributions are welcome! Please feel free to submit pull requests, create issues for bugs and feature requests, or provide feedback.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

[Lastic Telegram](https://t.me/+khw2i6GGYFw3NDNi)

Project Link: [https://github.com/lastic_xyz/price-sumulation](https://github.com/lastic_xyz/price-sumulation)

## Acknowledgments

- List any resources, libraries, or tools that were used in the creation of this project.
- Give credit to authors and contributors.
