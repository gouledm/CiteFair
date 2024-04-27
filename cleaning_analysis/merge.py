import pandas as pd

#Merges gender and nationality CSVs

genders_df = pd.read_csv('author_genders.csv')
nationalities_df = pd.read_csv('author_nationalities.csv')

if len(genders_df) != len(nationalities_df):
    raise ValueError("The CSV files do not have the same number of rows.")

genders_df['First Author Nationality'] = nationalities_df['First Author Nationality']
genders_df['Last Author Nationality'] = nationalities_df['Last Author Nationality']

combined_output_path = 'author_data.csv'
genders_df.to_csv(combined_output_path, index=False)

print(f"Combined data saved to {combined_output_path}")
