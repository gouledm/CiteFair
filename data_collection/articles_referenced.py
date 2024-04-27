from pymongo import MongoClient
import csv

# Gathers the articles referenced by the articles originally collected
# to later be stored in another collection in the database

client = MongoClient('mongodb://localhost:27017/')
db = client['crossref_metadata']
collection = db['articles']

def extract_referenced_dois():
    referenced_dois = set()  
    articles = collection.find({})

    for article in articles:
        if 'reference' in article:
            for reference in article['reference']:
                if 'DOI' in reference:
                    referenced_dois.add(reference['DOI'])

    return referenced_dois

def save_dois_to_csv(dois, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['DOI']) 
        for doi in dois:
            writer.writerow([doi])

if __name__ == "__main__":
    dois = extract_referenced_dois()
    save_dois_to_csv(dois, 'referenced_dois.csv')
    print(f"Extracted and saved {len(dois)} DOIs of referenced papers to CSV.")

