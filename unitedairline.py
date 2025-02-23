# -*- coding: utf-8 -*-
"""UNITEDAIRLINE.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZWvwmQkjHcc6xlSAArtnphUjTNUFCnrO
"""



"""#IMPORT LIBARIRES"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns

"""#LOAD DATASET"""

df=pd.read_csv("/content/drive/MyDrive/DATASET/Airline_Passenger_Data.csv")
df

"""# Display first few rows"""

print(df.head())

"""# Check for missing values"""

print(df.isnull().sum())

"""# Summary statistics"""

print(df.describe())

"""# Data types check"""

print(df.info())

"""# Convert Date column to datetime"""

df['Date'] = pd.to_datetime(df['Date'])

"""# Remove duplicate rows"""

df = df.drop_duplicates()

"""# Fix negative values in "First Class Passengers"
"""

df['First Class Passengers'] = df['First Class Passengers'].apply(lambda x: abs(x) if x < 0 else x)

"""# Verify changes"""

print(df.info())

print(df.describe())

"""# Set style"""

sns.set_style("whitegrid")

"""# Line plot: Total passengers over time"""

plt.figure(figsize=(12, 6))
sns.lineplot(x='Date', y='Total Passengers', data=df, marker='o')
plt.title("Total Passengers Over Time")
plt.xlabel("Date")
plt.ylabel("Total Passengers")
plt.xticks(rotation=45)
plt.show()

"""#Monthly Passenger Trends"""

df["Date"] = pd.to_datetime(df["Date"])  # Convert to datetime
df["Month"] = df["Date"].dt.month

plt.figure(figsize=(12, 6))
sns.lineplot(x="Month", y="Total Passengers", data=df, marker="o", color="b")
plt.title("Monthly Passenger Trend")
plt.xlabel("Month")
plt.ylabel("Number of Passengers")
plt.xticks(range(1, 13))
plt.show()

"""#Weekly Booking Trends"""

df["Day_of_Week"] = df["Date"].dt.day_name()

plt.figure(figsize=(12, 6))
sns.barplot(x=df["Day_of_Week"].value_counts().index, y=df["Day_of_Week"].value_counts(), palette="coolwarm")
plt.title("Weekly Booking Trends")
plt.ylabel("Bookings")
plt.show()

df.columns

"""#Ticket Price vs. Demand"""

plt.figure(figsize=(12, 6))
sns.scatterplot(x=df["Avg Ticket Price (USD)"], y=df["Total Passengers"], alpha=0.6)
plt.title("Ticket Price vs. Passenger Demand")
plt.xlabel("Ticket Price")
plt.ylabel("Number of Passengers")
plt.show()

plt.figure(figsize=(12, 6))
sns.scatterplot(x=df["Avg Ticket Price (USD)"], y=df["Economy Passengers"], alpha=0.6)
plt.title("Ticket Price vs. Passenger Demand")
plt.xlabel("Ticket Price")
plt.ylabel("Number of Passengers")
plt.show()

"""#Ticket Price vs. Economy Passengers Deamnd

# Correlation heatmap
"""

df.select_dtypes(exclude=['number']).columns

plt.figure(figsize=(10, 6))
sns.heatmap(df.select_dtypes(include=['number']).corr(), annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Feature Correlation Heatmap")
plt.show()

df_encoded = df.copy()
df_encoded = pd.get_dummies(df_encoded, drop_first=True)  # One-hot encoding

plt.figure(figsize=(10, 6))
sns.heatmap(df_encoded.corr(), annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Feature Correlation Heatmap")
plt.show()

"""#Monthly Passenger Trends

#Time Series Forecasting (ARIMA Model)
"""

from statsmodels.tsa.arima.model import ARIMA

"""# Set Date as index"""

df.set_index("Date", inplace=True)

"""# Train-Test Split"""

train_size = int(len(df) * 0.8)
train, test = df[:train_size], df[train_size:]

"""# Train ARIMA Model"""

model = ARIMA(train['Total Passengers'], order=(5,1,0))  # (p,d,q) parameters
model_fit = model.fit()

"""# Make Predictions"""

predictions = model_fit.forecast(steps=len(test))

"""# Plot Predictions vs Actual"""

plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Total Passengers'], label="Actual", color="blue")
plt.plot(test.index, predictions, label="Predicted", color="red", linestyle="dashed")
plt.title("Passenger Demand Forecasting")
plt.xlabel("Date")
plt.ylabel("Total Passengers")
plt.legend()
plt.show()