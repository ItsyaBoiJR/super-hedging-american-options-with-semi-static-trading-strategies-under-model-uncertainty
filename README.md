# Super-hedging American Options with Semi-static Trading Strategies under Model Uncertainty

## Overview

This repository contains the Python implementation of the paper **"Super-hedging American Options with Semi-static Trading Strategies under Model Uncertainty"** by Erhan Bayraktar and Zhou Zhou. The paper introduces a framework for determining the super-hedging price of American options in a discrete-time market, where stocks can be dynamically traded, and European options are available for static trading.

The core concept of the paper revolves around **super-hedging** under model uncertainty. The authors show that the super-hedging price of an American option can be expressed as the supremum over randomized models. This involves optimizing over martingale measures that correctly price the European options while allowing for the dynamic trading of stocks.

The provided code implements the key mathematical results and computational techniques outlined in the paper, enabling users to compute super-hedging prices for American options under the described framework.

---

## Key Concepts

The paper introduces the following ideas:

1. **Super-Hedging Price**:
   - The super-hedging price represents the minimum initial capital required to guarantee the replication of an American option payoff, regardless of the market model chosen.

2. **Semi-static Trading**:
   - The trading strategy consists of dynamic trading in stocks and static holdings in European options.

3. **Model Uncertainty**:
   - Instead of assuming a single probability model for the market, the framework allows for randomized models, represented by a convex combination of martingale measures.

4. **Representation of Super-Hedging Price**:
   - The super-hedging price \( \pi \) is expressed as:
     \[
     \pi = \sup_{(c_i, Q_i)_i} \sum_i c_i \phi^{Q_i}
     \]
     where \( c_i \geq 0 \), \( \sum_i c_i = 1 \), \( Q_i \) are martingale measures that price European options correctly, and \( \phi^{Q_i} \) represents the price of the American option under the model \( Q_i \).

---

## Features of the Code

The Python code provided in this repository implements the following:

1. **Market Model Representation**:
   - Models the discrete-time stock price evolution and incorporates European option pricing under martingale measures.

2. **Randomized Model Construction**:
   - Allows for constructing convex combinations of martingale measures to account for model uncertainty.

3. **American Option Pricing**:
   - Computes the price of an American option under a given martingale measure using backward induction.

4. **Super-Hedging Price Computation**:
   - Implements the optimization algorithm to compute the supremum of American option prices over randomized models, as described in the paper.

---

## Installation

To use the code in this repository, first ensure you have Python installed on your system. The required dependencies are listed in the `requirements.txt` file.

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/super-hedging-american-options.git
   cd super-hedging-american-options
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

---

## Usage

To compute the super-hedging price for an American option, follow these steps:

1. **Define Market Parameters**:
   - Specify the stock price dynamics and the European options available for static trading.

2. **Set Up American Option Payoff**:
   - Define the payoff function for the American option.

3. **Run the Computation**:
   - Use the provided functions in the code to compute the super-hedging price under model uncertainty.

Example usage:
```python
from super_hedging import compute_super_hedging_price

# Define market and option parameters
stock_prices = [100, 110, 90, ...]  # Example stock price path
european_options = [...]            # European options data
american_option_payoff = lambda x: max(x - 100, 0)  # Example payoff function

# Compute the super-hedging price
price = compute_super_hedging_price(stock_prices, european_options, american_option_payoff)
print(f"Super-hedging price: {price}")
```

---

## Repository Structure

```
super-hedging-american-options/
│
├── super_hedging/
│   ├── __init__.py
│   ├── market_model.py       # Defines the market model and dynamics
│   ├── european_options.py   # Handles the pricing of European options
│   ├── american_option.py    # Implements American option pricing
│   ├── optimization.py       # Optimization routines for super-hedging price computation
│   └── utils.py              # Utility functions
│
├── tests/
│   ├── test_market_model.py  # Unit tests for market model
│   ├── test_options.py       # Unit tests for option pricing
│   └── test_optimization.py  # Unit tests for optimization routines
│
├── README.md                 # Documentation
├── requirements.txt          # Python dependencies
└── LICENSE                   # License information
```

---

## Contributing

Contributions to improve the implementation or extend its functionality are welcome. Please follow these steps:

1. Fork the repository.
2. Create a new feature branch.
3. Make your changes and write tests.
4. Submit a pull request with a detailed description of the changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## References

- Erhan Bayraktar, Zhou Zhou, *Super-hedging American Options with Semi-static Trading Strategies under Model Uncertainty*. [arXiv:1604.04608](https://arxiv.org/pdf/1604.04608v2)

For further details, please refer to the research paper linked above.