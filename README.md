# Coretime Sale Price Calculator

This project provides a tool to calculate and visualize the sale price of Coretime over blocktime based on various parameters. It is implemented in Python and utilizes the Streamlit library for creating an interactive web application.

This repository is meant to be from [Lastic](https://lastic.xyz) for the entire community therefore it will be forever open source under the GPLv3 license. If there are some changes you want to see, or have disagreements with the implementation, feel free to open up an issue and/or contribute with a pull request.

## Features

- Interactive sliders to adjust sale parameters.
- Real-time graph visualization of sale prices over time.
- Configurable region lengths and lead-in lengths for sale price calculation.
- Adaptation of sale price based on the number of cores sold.

## Getting Started

### Installation

#### Using Docker Compose (Recommended for Production)

1. Clone the repository:
   ```sh
   git clone https://github.com/LasticXYZ/price-simulation.git
   cd price-simulation
   ```

2. Build and run the application using Docker Compose:
   ```sh
   docker-compose up --build
   ```

3. Access the application at `http://localhost:8501`.

4. To stop and remove the containers:
   ```sh
   docker-compose down
   ```

   Optionally, to remove volumes as well:
   ```sh
   docker-compose down -v
   ```

#### Using Python and Pip (Recommended for Development)

##### Prerequisites

- Python 3.x
- Pip (Python package installer)
- Docker (optional, for containerized deployment)
- Docker Compose (optional, for managing multi-container Docker applications)

##### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/LasticXYZ/price-simulation.git
   cd price-simulation
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```sh
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

    or install the main requirements with:
    ```sh
    pip install numpy matplotlib streamlit
    ```

4. Run the Streamlit application:
   ```sh
   streamlit run main.py
   ```

### Running Unit Tests

To run unit tests for this project, execute the following commands:

1. Install the required packages for testing:

    ```sh
    pip install -r requirements-test.txt
    ```

2. Run the tests:

    ```sh
    python -m unittest discover
    ```

This will execute all unit tests in the project.

### Usage

- Adjust the parameters using the sliders on the left panel.
- Observe the real-time changes in the sale price graph.
- The sale price is recalculated at the end of each region based on the number of cores sold.

## Configuration

You can configure various parameters of the sale price calculation in the `config.py` file. Please refer to the comments in the file for explanations of each parameter.

## Contributing

Contributions are welcome! Please feel free to submit pull requests, create issues for bugs and feature requests, or provide feedback.

## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details.

## Contact

[Lastic Telegram](https://t.me/+khw2i6GGYFw3NDNi)

Project Link: [https://github.com/lastic_xyz/price-sumulation](https://github.com/LasticXYZ/price-simulation)
