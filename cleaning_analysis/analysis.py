import pandas as pd

# Categorizes race and gender combinations, 
# calculates overall average citation count, 
# and calculates the average for each group

df = pd.read_csv('final_updated_data.csv')

def categorize_race(first_race, last_race):
    if first_race == 'White' and last_race == 'White':
        return 'WW'
    elif first_race == 'White' and last_race != 'White':
        return 'WC'
    elif first_race != 'White' and last_race == 'White':
        return 'CW'
    else:
        return 'CC'

def categorize_gender(first_gender, last_gender):
    if first_gender == 'male' and last_gender == 'male':
        return 'MM'
    elif first_gender == 'male' and last_gender == 'female':
        return 'MW'
    elif first_gender == 'female' and last_gender == 'male':
        return 'WM'
    else:
        return 'WW'

def categorize_gender_and_race(first_gender, last_gender, first_race, last_race):
    race_category = categorize_race(first_race, last_race)
    gender_category = categorize_gender(first_gender, last_gender)
    return race_category + ' + ' + gender_category

df['Race Category'] = df.apply(lambda x: categorize_race(x['First Author Race'], x['Last Author Race']), axis=1)
df['Gender Category'] = df.apply(lambda x: categorize_gender(x['First Author Gender'], x['Last Author Gender']), axis=1)
df['Combined Category'] = df.apply(lambda x: categorize_gender_and_race(x['First Author Gender'], x['Last Author Gender'], x['First Author Race'], x['Last Author Race']), axis=1)

overall_average = df['Citation Count'].mean()

average_citation_by_race = df.groupby('Race Category')['Citation Count'].mean()
average_citation_by_gender = df.groupby('Gender Category')['Citation Count'].mean()
average_citation_by_combined = df.groupby('Combined Category')['Citation Count'].mean()

print(f"Overall Average Citation Count: {overall_average:.2f}")
print("\nAverage Citation Count by Race Category:")
print(average_citation_by_race)
print("\nAverage Citation Count by Gender Category:")
print(average_citation_by_gender)
print("\nAverage Citation Count by Combined Race and Gender Category:")
print(average_citation_by_combined)

race_comparison = average_citation_by_race - overall_average
gender_comparison = average_citation_by_gender - overall_average
combined_comparison = average_citation_by_combined - overall_average

print("\nComparison of Race Category Averages to Overall Average:")
print(race_comparison)
print("\nComparison of Gender Category Averages to Overall Average:")
print(gender_comparison)
print("\nComparison of Combined Category Averages to Overall Average:")
print(combined_comparison)

# saves the new information in another CSV file
updated_csv_path = 'citation_analysis.csv'
df.to_csv(updated_csv_path, index=False)

print(f"\nUpdated data with race, gender, and combined categories and comparisons saved to {updated_csv_path}")
