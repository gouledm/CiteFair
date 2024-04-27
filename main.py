import requests

# Bias conditions based on analysis (see analysis.py and visual_analysis.py)
gender_bias_conditions = {
    'MM': 'biased',
    'MW': 'unbiased',
    'WM': 'unbiased',
    'WW': 'unbiased',
}

race_bias_conditions = {
    'CC': 'unbiased',
    'CW': 'biased',
    'WC': 'biased',
    'WW': 'biased',
}

# Gets first and last authors' names from crossref
def fetch_authors_from_crossref(doi):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        authors = data['message'].get('author', [])
        if authors:
            first_author = f"{authors[0].get('given', '')} {authors[0].get('family', '')}".strip()
            last_author = f"{authors[-1].get('given', '')} {authors[-1].get('family', '')}".strip() if len(authors) > 1 else first_author
            return first_author, last_author
    return None, None

def get_gender_race_from_namsor(full_name, api_key):
    # split the name for improved accuracy
    first_name, last_name = full_name.split(maxsplit=1)
    gender_url = f"https://v2.namsor.com/NamSorAPIv2/api2/json/gender/{first_name}/{last_name}"
    race_url = f"https://v2.namsor.com/NamSorAPIv2/api2/json/usRaceEthnicity/{first_name}/{last_name}"
    headers = {'X-API-KEY': api_key}
    
    # get gender
    gender_response = requests.get(gender_url, headers=headers)
    if gender_response.status_code == 200:
        gender_data = gender_response.json()
        gender = 'M' if gender_data.get('likelyGender') == 'male' else 'W' if gender_data.get('likelyGender') == 'female' else 'unknown'
    else:
        gender = 'unknown'

    # get race
    race_response = requests.get(race_url, headers=headers)
    if race_response.status_code == 200:
        race_data = race_response.json()
        race = 'W' if race_data.get('usRaceEth4') in ['W_NL', 'HL'] else 'C'
    else:
        race = 'unknown'
    return gender, race

# determines bias based on bias conditions
def determine_bias(first_author_gender, last_author_gender, first_author_race, last_author_race):
    gender_category = first_author_gender + last_author_gender
    race_category = first_author_race + last_author_race
    gender_bias = gender_bias_conditions.get(gender_category, 'unbiased')
    race_bias = race_bias_conditions.get(race_category, 'unbiased')

    return gender_bias, race_bias

if __name__ == "__main__":
    # key removed for security reasons
    api_key = 'api_key_here'  
    doi = input("Enter DOI: ")
    first_author_name, last_author_name = fetch_authors_from_crossref(doi)
    
    if first_author_name and last_author_name:
        first_author_gender, first_author_race = get_gender_race_from_namsor(first_author_name, api_key)
        last_author_gender, last_author_race = get_gender_race_from_namsor(last_author_name, api_key)

        gender_bias, race_bias = determine_bias(first_author_gender, last_author_gender, first_author_race, last_author_race)

        print(f"DOI: {doi}")
        print(f"First Author: {first_author_name}, Gender: {first_author_gender}, Race: {first_author_race}")
        print(f"Last Author: {last_author_name}, Gender: {last_author_gender}, Race: {last_author_race}")
        print(f"Gender Bias Result: {gender_bias}")
        print(f"Race Bias Result: {race_bias}")
    else:
        print("No authors found or an error occurred.")

