# Pseudocode
# 1. Ask user to input initial infected number and daily growth rate
# 2. Initialize days to 0, current infected count to initial value
# 3. Loop:
#    a. Print current day and infected count
#    b. If current infected count ≥ 91, stop the loop
#    c. Calculate infected count for the next day
#    d. Increase days by 1
# 4. Print total days required to infect the entire class

# Actual Code
# Ask user to input initial infected number and daily growth rate
initial_infected = float(input("Enter the initial number of infected students: "))
growth_rate = float(input("Enter the daily growth rate (e.g., enter 0.4 for 40%): "))

# Set variables
total_students = 91  # Total number of students in the class
current_infected = initial_infected
days = 0

# Print header
print(f"{'Day':<6}{'Infected Count':<15}")
print("-" * 21)

# Loop to calculate daily infected count
while True:
    # Print daily data
    print(f"{days:<6}{current_infected:<15.2f}")
    
    # If infected count ≥ 91, stop the loop
    if current_infected >= total_students:
        break

    # Calculate infected count for the next day
    current_infected = current_infected * (1 + growth_rate)
    days += 1

# Output total days
print(f"It takes {days} days to infect all {total_students} students in the class.")