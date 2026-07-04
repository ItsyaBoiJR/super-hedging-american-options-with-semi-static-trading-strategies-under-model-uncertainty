import numpy as np
import torch
from torch import nn
from torch.optim import Adam

class AmericanOptionHedging:
    def __init__(self, european_prices, payoff_function, num_models=10):
        """
        Initialize the super-hedging model.
        
        Args:
            european_prices (torch.Tensor): Prices of the European options.
            payoff_function (callable): Payoff function for the American option.
            num_models (int): Number of randomized models to consider.
        """
        self.european_prices = european_prices
        self.payoff_function = payoff_function
        self.num_models = num_models
        self.models = [self._create_model() for _ in range(num_models)]
        self.weights = torch.nn.Parameter(torch.ones(num_models) / num_models)
        self.optimizer = Adam(self.models_parameters() + [self.weights], lr=0.01)

    def _create_model(self):
        """
        Create a simple neural network to represent a martingale measure Q.
        """
        return nn.Sequential(
            nn.Linear(1, 16),
            nn.ReLU(),
            nn.Linear(16, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )

    def models_parameters(self):
        """
        Collect parameters from all models.
        """
        params = []
        for model in self.models:
            params += list(model.parameters())
        return params

    def price_european_options(self, stock_prices):
        """
        Compute the prices of European options under each model.
        
        Args:
            stock_prices (torch.Tensor): Simulated stock prices.
        
        Returns:
            torch.Tensor: Prices of European options under each model.
        """
        european_prices = []
        for model in self.models:
            european_prices.append(model(stock_prices).mean())
        return torch.stack(european_prices)

    def price_american_option(self, stock_prices):
        """
        Compute the price of the American option under each model.
        
        Args:
            stock_prices (torch.Tensor): Simulated stock prices.
        
        Returns:
            torch.Tensor: Prices of the American option under each model.
        """
        american_prices = []
        for model in self.models:
            discounted_payoffs = self.payoff_function(stock_prices) * model(stock_prices)
            american_prices.append(discounted_payoffs.mean())
        return torch.stack(american_prices)

    def train(self, stock_prices, num_epochs=1000):
        """
        Train the model to find the super-hedging price.
        
        Args:
            stock_prices (torch.Tensor): Simulated stock prices.
            num_epochs (int): Number of training epochs.
        """
        for epoch in range(num_epochs):
            self.optimizer.zero_grad()
            
            # Normalize weights
            weights = torch.softmax(self.weights, dim=0)
            
            # Price European options under each model
            european_prices = self.price_european_options(stock_prices)
            
            # Enforce the constraint that the weighted sum of model prices matches the market prices
            constraint_loss = torch.sum((weights @ european_prices - self.european_prices) ** 2)
            
            # Price American option under each model
            american_prices = self.price_american_option(stock_prices)
            
            # Compute the super-hedging price
            super_hedging_price = torch.dot(weights, american_prices)
            
            # Minimize negative super-hedging price (maximize the price)
            loss = -super_hedging_price + constraint_loss
            
            loss.backward()
            self.optimizer.step()
            
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {loss.item()}, Super-Hedging Price: {super_hedging_price.item()}")

    def get_super_hedging_price(self, stock_prices):
        """
        Get the super-hedging price after training.
        
        Args:
            stock_prices (torch.Tensor): Simulated stock prices.
        
        Returns:
            float: Super-hedging price.
        """
        weights = torch.softmax(self.weights, dim=0)
        american_prices = self.price_american_option(stock_prices)
        return torch.dot(weights, american_prices).item()

def american_option_payoff(stock_prices, strike_price):
    """
    Example payoff function for an American call option.
    
    Args:
        stock_prices (torch.Tensor): Simulated stock prices.
        strike_price (float): Strike price of the option.
    
    Returns:
        torch.Tensor: Payoff values.
    """
    return torch.maximum(stock_prices - strike_price, torch.zeros_like(stock_prices))

if __name__ == '__main__':
    # Simulated stock prices
    stock_prices = torch.linspace(50, 150, steps=100).unsqueeze(1)  # 100 stock prices between 50 and 150
    
    # Market prices of European options
    european_prices = torch.tensor([10.0, 15.0, 20.0])  # Example prices
    
    # Define payoff function for an American call option
    strike_price = 100
    payoff_function = lambda x: american_option_payoff(x, strike_price)
    
    # Initialize and train the model
    hedging_model = AmericanOptionHedging(european_prices, payoff_function, num_models=3)
    hedging_model.train(stock_prices, num_epochs=1000)
    
    # Get the super-hedging price
    super_hedging_price = hedging_model.get_super_hedging_price(stock_prices)
    print(f"Super-Hedging Price: {super_hedging_price}")