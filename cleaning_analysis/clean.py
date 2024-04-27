import pandas as pd

# Removes missing data if all fallbacks fail

df = pd.read_csv('updated_cleaned_author_data.csv')

cleaned_df = df.dropna()

cleaned_output_path = 'final_GR_data.csv'
cleaned_df.to_csv(cleaned_output_path, index=False)

print(f"Cleaned data saved to {cleaned_output_path}")
print(f"Removed {len(df) - len(cleaned_df)} rows with one or more blank cells.")
