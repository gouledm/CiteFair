import pandas as pd
from iso3166 import countries

# Converts country code to country name when needed (Using the ISO 3166-1 alpha 2 standard)

author_data_df = pd.read_csv('updated_author_data.csv')

def get_country_name(iso_code):
    if pd.isna(iso_code):
        return None
    try:
        return countries.get(iso_code).name
    except KeyError:
        print(f"No country found for ISO code: {iso_code}")
        return None

author_data_df['First Author Top Country Name'] = author_data_df['First Author Top Country'].apply(get_country_name)
author_data_df['Last Author Top Country Name'] = author_data_df['Last Author Top Country'].apply(get_country_name)

final_output_path = 'final_author_data.csv'
author_data_df.to_csv(final_output_path, index=False)

print(f"Final updated data saved to {final_output_path}")
