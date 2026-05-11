# Define the food_item class as specified in the practical guide
class food_item:
    def __init__(self, name, calories, protein, carbohydrates, fat):
        self.name = name
        self.calories = calories
        self.protein = protein
        self.carbohydrates = carbohydrates
        self.fat = fat

# Function to calculate 24-hour total nutrition and check for warnings
def calculate_nutrition(food_list):
    total_calories = 0
    total_protein = 0
    total_carbohydrates = 0
    total_fat = 0

    # Sum up all nutritional data from the consumed items
    for item in food_list:
        total_calories += item.calories
        total_protein += item.protein
        total_carbohydrates += item.carbohydrates
        total_fat += item.fat

    # Report the total results for the 24-hour period
    print("=== 24-Hour Nutritional Summary ===")
    print(f"Total Calories: {total_calories} kcal")
    print(f"Total Protein: {total_protein} g")
    print(f"Total Carbohydrates: {total_carbohydrates} g")
    print(f"Total Fat: {total_fat} g")

    # Check and report warnings based on the specified thresholds
    print("\n=== Nutritional Warnings ===")
    warning_triggered = False
    
    # Warning for excessive calories (> 2,500)
    if total_calories > 2500:
        print("Warning: Caloric intake exceeds 2,500 kcal!")
        warning_triggered = True
    
    # Warning for excessive fat (> 90 g)
    if total_fat > 90:
        print("Warning: Fat intake exceeds 90 g!")
        warning_triggered = True
        
    # If no thresholds are exceeded
    if not warning_triggered:
        print("All nutritional levels are within the normal range.")

# Example usage of the class and function for assessment
if __name__ == "__main__":
    # Example food item as described in the assignment (Apple: 60 cal, 0.3g pro, 15g carb, 0.5g fat)
    apple = food_item("Apple", 60, 0.3, 15, 0.5)
    
    # Additional items to simulate a 24-hour consumption list
    chicken = food_item("Chicken", 250, 30, 0, 8)
    rice = food_item("Rice", 200, 4, 45, 0.5)
    
    # List of food items consumed
    daily_consumption = [apple, chicken, rice]
    
    # Calling the function to report data and warnings
    calculate_nutrition(daily_consumption)