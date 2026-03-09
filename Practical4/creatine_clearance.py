# PSEUDOCODE
# 1. Get user inputs: age, weight (kg), gender (male/female), creatinine level (μmol/l)
# 2. Check if inputs are valid:
#    - Age < 100
#    - Weight between 20 and 80 kg
#    - Creatinine between 0 and 100 μmol/l
#    - Gender is only 'male' or 'female'
# 3. If inputs are invalid: show "Input variables need correction"
# 4. If inputs are valid: calculate Creatine Clearance (CrCl) with Cockcroft-Gault formula:
#    CrCl = ((140 - age) * weight) / (72 * creatinine)
#    - For female: multiply result by 0.85
# 5. Show the CrCl result

# Step 1: Get user inputs
age = int(input("Enter age (years): "))
weight = float(input("Enter weight (kg): "))
gender = input("Enter gender (male/female): ").lower()  # Make input lowercase
creatinine = float(input("Enter creatinine level (μmol/l): "))

# Step 2: Check input validity
is_valid = True

# Check age
if age >= 100:
    is_valid = False
    print("Age must be less than 100")

# Check weight
if weight < 20 or weight > 80:
    is_valid = False
    print("Weight must be between 20 and 80 kg")

# Check creatinine
if creatinine < 0 or creatinine > 100:
    is_valid = False
    print("Creatinine must be between 0 and 100 μmol/l")

# Check gender
if gender not in ['male', 'female']:
    is_valid = False
    print("Gender must be 'male' or 'female'")

# Step 3 & 4: Calculate CrCl if inputs are valid
if not is_valid:
    print("Input variables need correction")  # Show message if inputs are invalid
else:
    # Calculate basic CrCl with Cockcroft-Gault formula
    crcl = ((140 - age) * weight) / (72 * creatinine)
    
    # Adjust for female (multiply by 0.85)
    if gender == 'female':
        crcl = crcl * 0.85
    
    # Show result (round to 2 decimal places for readability)
    print("Creatine Clearance (CrCl): " + str(round(crcl, 2)) + " ml/min")