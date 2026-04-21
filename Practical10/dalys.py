# Step 1: Import all required libraries (follow guide)
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Step 2: Load CSV from same folder (no path change needed)
dalys_data = pd.read_csv("dalys-rate-from-all-causes.csv")

# Step 3: Basic dataframe inspection (follow guide)
print("===== Dataset Head (5 rows) =====")
print(dalys_data.head(5))

print("\n===== Dataset Info =====")
dalys_data.info()

print("\n===== DALYs Descriptive Statistics =====")
print(dalys_data["DALYs"].describe())

# Step 4: Show Year & DALYs (3rd & 4th columns) for first 10 rows
print("\n===== First 10 rows: Year & DALYs =====")
first_10 = dalys_data.iloc[0:10, [2, 3]]
print(first_10)

# Comment: Max DALYs year in Afghanistan first 10 records: 1998
afg_data = dalys_data[dalys_data["Entity"] == "Afghanistan"].iloc[0:10]
afg_max_year = afg_data.loc[afg_data["DALYs"].idxmax(), "Year"]

# Step 5: Boolean selection for Zimbabwe (follow guide)
zim_bool = dalys_data["Entity"] == "Zimbabwe"
zim_data = dalys_data.loc[zim_bool, ["Year", "DALYs"]]
print("\n===== Zimbabwe Data (first 5 rows) =====")
print(zim_data.head())
# Comment: Zimbabwe data period: 1990 - 2019

# Step 6: Get 2019 max & min DALYs countries (follow guide)
recent_data = dalys_data.loc[dalys_data.Year == 2019, ["Entity", "DALYs"]]
max_country = recent_data.loc[recent_data["DALYs"].idxmax(), "Entity"]
min_country = recent_data.loc[recent_data["DALYs"].idxmin(), "Entity"]
print("\n===== 2019 Results =====")
print(f"Country with highest DALYs: {max_country}")
print(f"Country with lowest DALYs: {min_country}")

# Step 7: Plot trend for max & min country in ONE figure
max_trend = dalys_data[dalys_data["Entity"] == max_country]
min_trend = dalys_data[dalys_data["Entity"] == min_country]

plt.figure(figsize=(10, 6))
plt.plot(max_trend.Year, max_trend.DALYs, "r-o", label=f"Highest: {max_country}")
plt.plot(min_trend.Year, min_trend.DALYs, "b-o", label=f"Lowest: {min_country}")
plt.xlabel("Year")
plt.ylabel("DALYs Rate")
plt.title("DALYs Trend: 2019 Highest vs Lowest Countries")
plt.legend()
plt.xticks(rotation=-45)
plt.savefig("max_min_trend.png")
plt.close()

# Step 8: Self-defined task (follow guide question)
# Question: What was the distribution of DALYs across all countries in 2019?
plt.figure(figsize=(8, 5))
plt.hist(recent_data["DALYs"].dropna(), bins=20, color="skyblue", edgecolor="black")
plt.xlabel("DALYs Rate")
plt.ylabel("Number of Countries")
plt.title("Distribution of DALYs Across All Countries in 2019")
plt.savefig("2019_dalys_distribution_hist.png")
plt.close()