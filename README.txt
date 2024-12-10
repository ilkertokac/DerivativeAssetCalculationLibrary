PyDerivativeLib: Option and Derivative Pricing Library

PyDerivativeLib is a Python library that provides a comprehensive set of classes for calculating option and derivative prices, as well as various Greeks and sensitivity measures. It also includes tools for simulating and visualizing the relationships between option prices and underlying asset prices.

Alternatively, you can clone the repository or download the code and include it in your project directory.
Usage
Option and Derivative Calculations

You can use the provided classes to calculate option and derivative prices, as well as various Greeks (sensitivity measures) such as Delta, Theta, Vega, Rho, and Gamma. Here's an example usage:

python

from PyDerivativeLib import OptionCalculate

# Create an option object
option = OptionCalculate(
    Type="P",
    UnderlyingPrice=10,
    StrikePrice=10,
    DaysToMaturity=10,
    DomesticRate=10,
    ImpliedVolatility=50,
    Dividend=0
)

# Calculate the option price
price = option.Price()
print(f"Option Price: {price:.6f}")

Visualizing Option-Underlying Price Relationship

You can also use the provided Graphs class to simulate and visualize the relationships between option prices and underlying asset prices. Here's an example usage:

python

from PyDerivativeLib import Graphs, Graph_Case

# Create a Graphs object
option_graph = Graphs(
    Type="Option",
    Asset_Type="C",
    UnderlyingPrice=10,
    StrikePrice=10,
    DaysToMaturity=10,
    DomesticRate=10,
    ImpliedVolatility=50,
    Dividend=0
)

# Generate and display a Delta graph
option_graph.DerivativeToolSimulationGraph(
    GraphCase=Graph_Case.Delta,
    percentage_change=0.05
)

Contributions

Contributions are welcome! If you find any issues or want to add new features, please submit a pull request.
Credits

This library was developed by [İlker Tokaç] and inspired by options and derivatives pricing theories.

