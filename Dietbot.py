import pandas as pd
from textblob import TextBlob

# Load your dataset
diet_df = pd.read_csv("Diet Data.csv")

print("Hi, I'm Dietbot.")
print("I will help you with a diet choice according to your health condition.\n")

# Collect user input
problem = input("What is your Health Condition(Arthritis/Asthma/Back Pain/Constipation/Diabetes/Fine/High BP/Low BP/Migraine) - ").lower()
name = input("Enter your name - ")
age = int(input("Enter your age - "))
weight = float(input("Enter your weight (in kg) - "))
height = float(input("Enter your height (in m) - "))
meal_type = input("Meal Type (Breakfast/Lunch/Dinner) - ").lower()
diet_type = input("Diet Type (Veg/Non-Veg) - ").lower()
budget_type = input("Budget (Low/Medium/High) - ").lower()

# Calculate BMI
BMI = weight / height**2

# Determine activity level
if 18.5 <= BMI <= 20.9:
    activity_level = "Sedentary"
    print(f"\nYour BMI is {BMI:.2f}; which is considered as {activity_level}.")
    print("It means you engage in minimal physical activity and spend most of the day sitting, with little to no structured exercise.")

elif 21.0 <= BMI <= 22.4:
    activity_level = "Lightly Active"
    print(f"\nYour BMI is {BMI:.2f}; which is considered as {activity_level}.")
    print("It means you perform light physical activity or exercises 1–3 days per week, such as walking or casual sports.")

elif 22.5 <= BMI <= 23.9:
    activity_level = "Moderately Active"
    print(f"\nYour BMI is {BMI:.2f}; which is considered as {activity_level}.")
    print("It means you participate in moderate-intensity exercise or sports 3–5 days per week, involving consistent movement.")

elif 24.0 <= BMI <= 26.0:
    activity_level = "Very Active"
    print(f"\nYour BMI is {BMI:.2f}; which is considered as {activity_level}.")
    print("It means you engage in intense physical activity or exercise 6–7 days a week or have a physically demanding job.")

else:
    print(f"\nYour BMI is {BMI:.2f}.")
    print("BMI not in the healthy range for any activity level.")
    activity_level = None  # Handle cases outside defined range

# Filter only if BMI is in known range
if activity_level:
    filtered_df = diet_df[
        (diet_df['Activity Level'].str.lower().str.contains(activity_level.lower())) &
        (diet_df['Health Condition'].str.lower() == problem) &
        (diet_df['Budget'].str.lower() == budget_type) &
        (diet_df['Meal Type'].str.lower() == meal_type) &
        (diet_df['Diet Type'].str.lower() == diet_type)
    ]

    # Display suggestions
    if not filtered_df.empty:
        print("\n Suggested Meals:")
        for index, row in filtered_df.iterrows():
            print(f"- {row['Dish Name']} ({row['Calories (in g)']} Calories, {row['Protein (in g)']} Protein)")
    else:
        print("\n No matching meals found. Try changing your preferences.")
