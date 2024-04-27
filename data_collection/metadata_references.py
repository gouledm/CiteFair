import requests
import csv
from pymongo import MongoClient

#Collecting metadata of articles referenced by the original set

client = MongoClient('mongodb://localhost:27017/')
db = client['crossref_metadata']
collection = db['articles_references']

def fetch_metadata(doi):
    url = f'https://api.crossref.org/works/{doi}'
    headers = {'User-Agent': 'youremail@gmail.com'} 
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch metadata for DOI {doi}: {response.status_code}")
        return None

def get_publication_year(metadata):
    try:
        year = metadata['message']['issued']['date-parts'][0][0]
        return int(year)  
    except (KeyError, IndexError, TypeError, ValueError):
        print(f"Unable to find or parse publication year for DOI.")
        return None

# Filtering them to only keep articles published in the last 10 years
def save_metadata_to_mongodb(metadata):
    year = get_publication_year(metadata)
    if year and year >= 2013:
        if collection.count_documents({}) < 12500:
            try:
                result = collection.insert_one(metadata['message'])
                print(f"Metadata for DOI inserted with ID: {result.inserted_id}")
                return True
            except Exception as e:
                print(f"Error inserting into MongoDB: {e}")
        else:
            print("Reached the limit of 12,500 entries.")
            return False
    else:
        print(f"Skipping DOI, published in {year} or invalid year.")
    return True

def process_dois(csv_file):
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            if row:
                doi = row[0]
                metadata = fetch_metadata(doi)
                if metadata:
                    if not save_metadata_to_mongodb(metadata):
                        break 

if __name__ == "__main__":
    process_dois('referenced_dois.csv')
