# Define food item class
class FoodItem:
    def __init__(self, name, calories, protein, carbs, fat):
        self.name = name
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat

# Calculate total nutrition and check warnings
def calculate_nutrition(food_list):
    total_cal = 0
    total_pro = 0
    total_car = 0
    total_fat = 0

    # Sum all nutrition data
    for food in food_list:
        total_cal += food.calories
        total_pro += food.protein
        total_car += food.carbs
        total_fat += food.fat

    # Print total results
    print("=== 24H Total Nutrition ===")
    print(f"Calories: {total_cal} kcal")
    print(f"Protein: {total_pro} g")
    print(f"Carbohydrates: {total_car} g")
    print(f"Fat: {total_fat} g")

    # Print warnings
    print("\n=== Warnings ===")
    if total_cal > 2500:
        print("Warning: Calories exceed 2500 kcal!")
    if total_fat > 90:
        print("Warning: Fat exceed 90 g!")
    if total_cal <= 2500 and total_fat <= 90:
        print("No warnings, nutrition intake is normal.")

# Main execution
if __name__ == "__main__":
    # Example (required by the task)
    print("This is an example:\n")
    food1 = FoodItem("Rice", 200, 4, 45, 0.5)
    food2 = FoodItem("Chicken", 250, 30, 0, 8)
    food3 = FoodItem("Apple", 95, 0.5, 22, 0.3)
    daily_food = [food1, food2, food3]
    calculate_nutrition(daily_food)