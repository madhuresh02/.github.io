import pandas as pd
from textblob import TextBlob  # (not used, you can remove if you want)

# ---- Load & normalize dataset ------------------------------------------------
diet_df = pd.read_csv("Diet Data.csv")
# tidy headers
diet_df.columns = diet_df.columns.str.strip().str.lower()

# normalize some common text columns if they exist
for col in ["meal type", "diet type", "budget", "health condition", "bmi goal"]:
    if col in diet_df.columns:
        diet_df[col] = diet_df[col].astype(str).str.strip().str.lower().str.replace("-", " ")

# figure out which columns represent calories/protein (synonyms allowed)
def first_present(cols, options):
    for opt in options:
        if opt in cols:
            return opt
    return None

cal_col = first_present(
    diet_df.columns,
    ["calories", "calorie", "kcal", "energy (kcal)", "energy"]
)
prot_col = first_present(
    diet_df.columns,
    ["protein", "proteins", "protein (g)", "protien"]  # include common misspellings
)

# check essential columns
required = ["meal type", "dish name", "diet type", "budget", "health condition"]
missing = [c for c in required if c not in diet_df.columns]
if missing:
    raise ValueError(f"CSV is missing required column(s): {missing}. "
                     f"Found columns: {list(diet_df.columns)}")

print("Hi, I'm Dietbot.")
print("I will help you with a diet choice according to your health condition.\n")

# ---- Collect user input ------------------------------------------------------
problem = input("What is your Health Condition (Arthritis/Asthma/Back Pain/Constipation/Diabetes/Fine/High BP/Low BP/Migraine) - ").lower().strip().replace("-", " ")
name = input("Enter your name - ")
age = int(input("Enter your age - "))
weight = float(input("Enter your weight (in kg) - "))
height = float(input("Enter your height (in m) - "))
meal_type = input("Meal Type (Breakfast/Lunch/Dinner) - ").lower().strip()
diet_type = input("Diet Type (Veg/Non-Veg) - ").lower().strip().replace("-", " ")
budget_type = input("Budget (Low/Medium/High) - ").lower().strip()

# ---- BMI & activity info (your existing logic) -------------------------------
BMI = weight / (height ** 2)

if 18.5 <= BMI <= 20.9:
    activity_level = "Sedentary"
    print(f"\nYour BMI is {BMI:.2f}; which is considered as Sedentary.")
    print("It means you engage in minimal physical activity and spend most of the day sitting, with little to no structured exercise.")
elif 21.0 <= BMI <= 22.4:
    activity_level = "Lightly Active"
    print(f"\nYour BMI is {BMI:.2f}; which is considered as Lightly Active.")
    print("It means you perform light physical activity or exercises 1–3 days per week, such as walking or casual sports.")
elif 22.5 <= BMI <= 23.9:
    activity_level = "Moderately Active"
    print(f"\nYour BMI is {BMI:.2f}; which is considered as Moderately Active.")
    print("It means you participate in moderate-intensity exercise or sports 3–5 days per week, involving consistent movement.")
elif 24.0 <= BMI <= 26.0:
    activity_level = "Very Active"
    print(f"\nYour BMI is {BMI:.2f}; which is considered as Very Active.")
    print("It means you engage in intense physical activity or exercise 6–7 days a week or have a physically demanding job.")
else:
    activity_level = None
    print(f"\nYour BMI is {BMI:.2f}.")
    print("BMI not in the healthy range for any activity level.")

# ---- Optional BMI Goal step --------------------------------------------------
bmi_choice = input(
    "\nDo you want to Increase, Decrease, Maintain (or Same) your BMI? "
    "Press Enter to skip: "
).lower().strip()

# map 'same' to 'maintain'
if bmi_choice == "same":
    bmi_choice = "maintain"

use_bmi_goal = (bmi_choice in ["increase", "decrease", "maintain"]) and ("bmi goal" in diet_df.columns)
if use_bmi_goal:
    bmi_goal_value = f"{bmi_choice} bmi"

# ---- Build filter mask -------------------------------------------------------
mask = (
    (diet_df["meal type"] == meal_type) &
    (diet_df["diet type"] == diet_type) &
    (diet_df["budget"] == budget_type) &
    (diet_df["health condition"] == problem)
)

if use_bmi_goal:
    mask = mask & (diet_df["bmi goal"] == bmi_goal_value)

filtered_df = diet_df.loc[mask].copy()

# ---- Display results safely (no KeyErrors if cols absent) --------------------
if not filtered_df.empty:
    print("\nSuggested Meals:")
    for _, row in filtered_df.iterrows():
        details = []
        if cal_col in filtered_df.columns and pd.notna(row.get(cal_col, None)):
            details.append(f"{row[cal_col]} Calories")
        if prot_col in filtered_df.columns and pd.notna(row.get(prot_col, None)):
            details.append(f"{row[prot_col]} Protein")
        if details:
            print(f"- {row['dish name']} ({', '.join(details)})")
        else:
            print(f"- {row['dish name']}")
else:
    print("\nNo matching meals found. Try changing your preferences.")
