# Automated Tests for Online Shop using Selenium

This project contains automated tests for an online shop using the Selenium framework. The tests are designed to verify the functionality and behavior of the online shop application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Tests](#running-the-tests)
- [Test Cases](#test-cases)
- [Contributing](#contributing)

## Prerequisites

To run the automated tests, you need to have the following software installed:

- Python (version 3.7 or higher)
- Selenium Python bindings (`selenium` package)
- Webdriver for the browser you intend to automate (e.g., ChromeDriver for Google Chrome)

## Setup

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/illanacohen/online-shop-testing.git
   ```

2. Navigate to the project directory:

   ```bash
   cd online-shop-testing
   ```

3. Install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. Download and install the appropriate WebDriver for your browser. Make sure the WebDriver executable is added to your system's PATH.

## Running the Tests

To run the tests, execute the following command from the project directory:

```bash
python test.py --scenarios '{<service1>: [<scenario1>, <scenario2>]}'
```
where service1 could be on the following:

```bash
'braintree'
'stripe'
```

and scenario1 could be one or more of the following:

```bash
'scenario-Successful transaction'
'scenario-Declined transaction declined'
'scenario-Declined transaction approved'
```

This command will execute all the test cases defined in the `tests` directory for the given scenarios.

## Test Cases

The `test` directory contains one test case `test.py`. To cover different scenarios of the online shop application, you must give arguments to `--scenarios`.

## Contributing

Contributions to this project are welcome! If you find any issues or want to add new features, please submit a pull request. Make sure to follow the coding style and include appropriate test cases for your changes.

---
