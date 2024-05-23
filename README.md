# autohyp

## Description

When working with clinical data, we often want to compare variables between two patient populations. For example, how do all the clinical variables differ between patients who have a history of smoking vs. non-smokers? To do this we need to perform different statistical tests depending on the variable.

* for binary variables (ex: mortality) we use a two-proportion z-test
* for normally distributed continuous variables (ex: heart rate) we use a t-test
* for skewed continuous variables (ex: MEU) we use a Mann-Whitney test

Manually doing these tests for many variables can be a tedious task. Autohyp automates these hypothesis tests. By simply uploading an Excel sheet, you can now compare all variables in your data set between two patient groups.

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yashacode/autohyp.git
    cd your-repository
    ```

2. **Create and activate a virtual environment (optional but strongly recommended):**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

```sh
python main.py

```

## Authors

Jacob Epstein

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
