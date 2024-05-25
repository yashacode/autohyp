# autohyp

## Description

When working with clinical data, we often want to compare variables between two patient populations. For example, how do all the clinical variables differ between patients who have a history of smoking vs. non-smokers? To do this we need to perform different statistical tests depending on the variable.

* for binary variables (ex: mortality) we use a two-proportion z-test
* for normally distributed continuous variables (ex: heart rate) we use a t-test
* for skewed continuous variables (ex: MEU) we use a Mann-Whitney test

Manually doing these tests for many variables can be a tedious task. Autohyp automates these hypothesis tests. By simply uploading an Excel sheet, you can now compare all variables in your data set between two patient groups.

## Installation

Open the terminal on Mac or the command line on Windows.

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yashacode/autohyp.git
    cd autohyp
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

1. **Create Ecxel document**
Autohyp requires an Excel file as input. The file should have the following format:

* The first row must contain all the variable names (Age, heart rate, etc...)
* Each subsequent row contains the clinical data for a single patient. All entries below the first row must be numeric (for binary variables such as mortality, use 1 for yes and 0 for no)

Copy the path of your Excel doc. Finder > Right-click your file > Show info > Right-click where section > Copy file path

2. **Run autohyp**

Go back to the autohyp directory in the terminal. Then run the following:

    
    python3 autohyp.py path/yourfile.xlsx
    
Replace path/yourfile.xlsx with the path you copied in the previous step. Once you run this, all the variables should be printed out in the terminal. You now must choose how to split the patients into two groups. For example, if you choose a binary variable like past medical history of smoking (with 0s and 1s as entries), the patients will be split into smokers and non-smokers. If you chose a continuous variable, you must type in a numeric value for splitting. For example, if you choose systolic blood pressure (SBP), you will be prompted for a value. If you then enter 120, the patients will be split into one group with SBP <= 120 and another with SBP > 120. Comparisons of all the variables will be done between these two groups.

```sh
enter the column used for comparison: past medical history of smoking

```

Make sure the column you enter matches one of the columns from the Excel sheet exactly.

2. **Collect results**

You should now have a file called output.xlsx with the results of the hypothesis tests. Each row corresponds to a different variable. The file is separated into 3 sheets for the 3 variable types (categorical, normal continuous, and non-normal continuous).

## Authors

Jacob Epstein

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
