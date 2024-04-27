import requests
import pandas as pd

# Country prediction based on the author's name using nationlize.io
# ethnicolr is used instead for racially diverse countries (see ethnicolr_prep.py)

df = pd.read_csv('author_genders.csv')

# API key removed for security reasons
api_key = 'api_key_here'

def predict_nationality(name):
    url = 'https://api.nationalize.io'
    params = {'name': name, 'apikey': api_key}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() 
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}, name: {name}")
        return None

def get_last_or_full_name(full_name):
    if pd.isna(full_name) or not full_name.strip():
        return None
    parts = full_name.strip().split()
    return parts[-1] if len(parts) > 1 else full_name

results = []

for index, row in df.iterrows():
    first_author_name = get_last_or_full_name(row['First Author'])
    last_author_name = get_last_or_full_name(row['Last Author'])
    results.append({
        'First Author Name': first_author_name,
        'First Author Nationality': predict_nationality(first_author_name) if first_author_name else None,
        'Last Author Name': last_author_name,
        'Last Author Nationality': predict_nationality(last_author_name) if last_author_name else None
    })

    if index % 100 == 0:
        print(f"Processed {index + 1} rows.")

nationality_df = pd.DataFrame(results)

# saves to a new CSV
nationality_df.to_csv('author_nationalities.csv', index=False)

print("Nationality predictions completed and saved.")
