import requests
import csv
from pymongo import MongoClient

# Getting the metadata from crossref of the original set of articles taken from IEEE

client = MongoClient('mongodb://localhost:27017/')
db = client['crossref_metadata']
collection = db['articles']

def fetch_metadata(doi):
    
    url = f'https://api.crossref.org/works/{doi}'
    headers = {'User-Agent': 'youremail@gmail.com'}  
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch metadata for DOI {doi}: {response.status_code}")
        return None

def save_metadata_to_mongodb(metadata):
    if metadata:
        try:
            result = collection.insert_one(metadata['message'])
            print(f"Metadata for DOI inserted with ID: {result.inserted_id}")
        except Exception as e:
            print(f"Error inserting into MongoDB: {e}")

def process_dois(csv_file):
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            if row:
                doi = row[0]
                metadata = fetch_metadata(doi)
                if metadata:
                    save_metadata_to_mongodb(metadata)

if __name__ == "__main__":
    csv_file = 'referenced_dois.csv' 
    process_dois(csv_file)
