# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file from the same folder
df = pd.read_csv("dalys-rate-from-all-causes.csv")

# Required output: Basic dataset check
print("===== Dataset Head =====")
print(df.head())
print("\n===== Dataset Info =====")
df.info()
# Required: Only show DALYs statistics
print("\n===== DALYs Descriptive Statistics =====")
print(df["DALYs"].describe())

# 1. Required: First 10 rows (Year and DALYs)
print("\n===== First 10 Rows (Year & DALYs) =====")
first_10 = df.iloc[:10, [2, 3]]
print(first_10)

# Comment: Max DALYs year for Afghanistan in first 10 records: 1998
afg_data = df[df["Entity"] == "Afghanistan"].iloc[:10]
afg_max_year = afg_data.loc[afg_data["DALYs"].idxmax(), "Year"]

# 2. Required: Select all data for Zimbabwe
print("\n===== Zimbabwe Data (First 5 Rows) =====")
zim_data = df[df["Entity"] == "Zimbabwe"][["Year", "DALYs"]]
print(zim_data.head())
# Comment: Zimbabwe data time range: 1990 - 2019

# 3. Required: Max and Min DALYs countries in 2019
data_2019 = df[df["Year"] == 2019]
max_country = data_2019.loc[data_2019["DALYs"].idxmax(), "Entity"]
min_country = data_2019.loc[data_2019["DALYs"].idxmin(), "Entity"]
print(f"\n===== 2019 Results =====")
print(f"Country with highest DALYs: {max_country}")
print(f"Country with lowest DALYs: {min_country}")

# 4. Required: Plot trend for max and min country in ONE figure + save
max_trend = df[df["Entity"] == max_country]
min_trend = df[df["Entity"] == min_country]

plt.figure(figsize=(10, 6))
plt.plot(max_trend["Year"], max_trend["DALYs"], "r-o", label=f"Highest: {max_country}")
plt.plot(min_trend["Year"], min_trend["DALYs"], "b-o", label=f"Lowest: {min_country}")
plt.xlabel("Year")
plt.ylabel("DALYs Rate")
plt.title("DALYs Trend (2019 Highest vs Lowest Countries)")
plt.legend()
plt.xticks(rotation=45)
plt.savefig("max_min_trend.png")
plt.close()

# Self-defined Task (Required)
# Question: What was the distribution of DALYs across all countries in 2019?
plt.figure(figsize=(8, 5))
# Use histogram for more intuitive distribution
plt.hist(data_2019["DALYs"].dropna(), bins=20, color="skyblue", edgecolor="black")
plt.xlabel("DALYs Rate")
plt.ylabel("Number of Countries")
plt.title("Distribution of DALYs Across All Countries in 2019")
plt.savefig("2019_dalys_distribution_hist.png")
plt.close()