import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Calculates averages and generates graphs

df = pd.read_csv('citation_analysis.csv')

overall_average = df['Citation Count'].mean()

# calculates the disparity
def calc_difference_from_overall(category, average):
    return category - overall_average

average_citation_by_race = df.groupby('Race Category')['Citation Count'].mean()
average_citation_by_gender = df.groupby('Gender Category')['Citation Count'].mean()
average_citation_by_combined = df.groupby('Combined Category')['Citation Count'].mean()

gender_diff = average_citation_by_gender.apply(calc_difference_from_overall, average=overall_average)
race_diff = average_citation_by_race.apply(calc_difference_from_overall, average=overall_average)
combined_diff = average_citation_by_combined.apply(calc_difference_from_overall, average=overall_average)

# Gender graph
plt.figure(figsize=(10, 6))
sns.barplot(x=gender_diff.index, y=gender_diff.values)
plt.axhline(0, color='black', linewidth=1.5, linestyle='--')
plt.title('Deviation from Overall Average Citation Count by Gender Category')
plt.ylabel('Deviation from Overall Average')
plt.xlabel('Gender Category')
plt.savefig('gender_deviation_plot.png')
plt.show()

# Race graph
plt.figure(figsize=(10, 6))
sns.barplot(x=race_diff.index, y=race_diff.values)
plt.axhline(0, color='black', linewidth=1.5, linestyle='--')
plt.title('Deviation from Overall Average Citation Count by Race Category')
plt.ylabel('Deviation from Overall Average')
plt.xlabel('Race Category')
plt.savefig('race_deviation_plot.png')
plt.show()

# Combined graph
plt.figure(figsize=(12, 8))
sns.barplot(x=combined_diff.index, y=combined_diff.values)
plt.axhline(0, color='black', linewidth=1.5, linestyle='--')
plt.title('Deviation from Overall Average Citation Count by Combined Race and Gender Category')
plt.ylabel('Deviation from Overall Average')
plt.xlabel('Combined Category')
plt.xticks(rotation=90)
plt.savefig('combined_deviation_plot.png')
plt.show()

