import math as m
import yfinance as yf
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

ticker = input("Enter the ticker you would like to run the simulation on: ")
#Convert each ticker into proper format
ticker = ticker.strip().upper()  

# Download data and convert series values into float values.
data = yf.download(ticker, period="max")
todays_price = float(data['Close'].iloc[-1])
yesterdays_price = float(data['Close'].iloc[-2])


num_trading_days = data['Close'].count()

log_returns = np.log(data['Close'] / data['Close'].shift(1))

# Drop any missing values
log_returns = log_returns.dropna()

variance = np.var(log_returns)

# Calculate the average daily return 
periodic_daily_return = m.log(todays_price/yesterdays_price)
average_daily_return = log_returns.mean()


average_price = data['Close'].mean()

# Drift from geometric brownian motion
drift = average_daily_return - (variance/2)

standard_deviation = log_returns.std()

predicted_price = [todays_price]

num_days = int(input("Enter the number of days you would like to simulate: "))
num_sims = int(input("Enter the number of simulations you would like to run: "))

all_simulations = []

for _ in range(num_sims):
    predicted_price = [todays_price]
    for _ in range(num_days):
        random_value = np.random.normal() * standard_deviation
        current_price = predicted_price[-1]
        next_days_price = current_price * m.exp(drift + random_value)
        predicted_price.append(next_days_price)
        all_simulations.append(predicted_price)
else: print("Simulation complete!")



plt.figure(figsize=(10, 5))

for sim in all_simulations:
    plt.plot(sim, alpha=.5)
    

# Now adjust the y-axis AFTER plotting
# Flatten all prices from all simulations into one list
all_prices = [price for sim in all_simulations for price in sim]
min_price = min(all_prices)
max_price = max(all_prices)
plt.ylim(min_price * 0.9, max_price * 1.1)  # A gentler, more visible buffer

plt.title(f"Simulated Stock Price for {ticker}")
plt.xlabel("Days")
plt.ylabel("Price")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()





