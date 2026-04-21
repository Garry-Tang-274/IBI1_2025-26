# Import libraries
import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file from the same folder
df = pd.read_csv("dalys-rate-from-all-causes.csv")

# Basic data check
print(df.head())
print(df.describe())

# 1. First 10 rows: Year and DALYs
top10 = df.iloc[:10, [2, 3]]
print("First 10 rows:\n", top10)

# 2. Filter data for Zimbabwe
zim = df[df["Entity"] == "Zimbabwe"][["Year", "DALYs"]]
print("Zimbabwe data:\n", zim.head())

# 3. Max and min DALYs countries in 2019
data2019 = df[df["Year"] == 2019]
max_country = data2019.loc[data2019["DALYs"].idxmax(), "Entity"]
min_country = data2019.loc[data2019["DALYs"].idxmin(), "Entity"]
print(f"2019 Max: {max_country}, Min: {min_country}")

# 4. Plot trend for max country
max_data = df[df["Entity"] == max_country]
plt.plot(max_data["Year"], max_data["DALYs"])
plt.title(f"DALYs Trend: {max_country}")
plt.xlabel("Year")
plt.ylabel("DALYs")
plt.show()

# 5. Self-defined task: China vs UK trend
cn = df[df["Entity"] == "China"]
uk = df[df["Entity"] == "United Kingdom"]
plt.plot(cn["Year"], cn["DALYs"], label="China")
plt.plot(uk["Year"], uk["DALYs"], label="UK")
plt.legend()
plt.title("China vs UK DALYs")
plt.show()