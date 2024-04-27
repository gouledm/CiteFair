import requests
import pandas as pd
from pymongo import MongoClient

# sourcing metadata from the database
client = MongoClient('mongodb://localhost:27017/')
db = client['crossref_metadata']
collection = db['articles_references']

# Using genderize first
def get_gender_from_genderize(name, api_key):
    url = "https://api.genderize.io/"
    params = {'name': name, 'apikey': api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200 and response.json().get('gender'):
        return response.json()['gender']
    return None

# and Namsor as a fallback whenever genderize failed
def get_gender_from_namsor(first_name, last_name, api_key):
    url = f"https://v2.namsor.com/NamSorAPIv2/api2/json/gender/{first_name}/{last_name}"
    headers = {'X-API-KEY': api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if result.get('likelyGender'):
            return result['likelyGender']
    return None

def process_articles(start_index, end_index, genderize_api_key, namsor_api_key):
    articles = collection.find().skip(start_index).limit(end_index - start_index)
    data_to_save = []

    for article in articles:
        doi = article.get('DOI', 'No DOI Found')
        authors = article.get('author', [])

        if len(authors) > 0:
            first_author = authors[0].get('given', '') + ' ' + authors[0].get('family', '')
            last_author = authors[-1].get('given', '') + ' ' + authors[-1].get('family', '') if len(authors) > 1 else first_author

            first_author_gender = get_gender_from_genderize(authors[0].get('given', ''), genderize_api_key)
            last_author_gender = get_gender_from_genderize(authors[-1].get('given', ''), genderize_api_key) if len(authors) > 1 else first_author_gender

            if not first_author_gender:
                first_author_gender = get_gender_from_namsor(authors[0].get('given', ''), authors[0].get('family', ''), namsor_api_key)
            if not last_author_gender and len(authors) > 1:
                last_author_gender = get_gender_from_namsor(authors[-1].get('given', ''), authors[-1].get('family', ''), namsor_api_key)

            data_to_save.append([doi, first_author, last_author, first_author_gender, last_author_gender])

    df = pd.DataFrame(data_to_save, columns=['DOI', 'First Author', 'Last Author', 'First Author Gender', 'Last Author Gender'])
    df.to_csv('author_genders_remaining.csv', index=False)

if __name__ == "__main__":
    # key removed for security reasons
    genderize_api_key = 'api_key_here'  
    namsor_api_key = 'api_key_here'  
    start_index = 50  
    end_index = 12500  
    process_articles(start_index, end_index, genderize_api_key, namsor_api_key)
