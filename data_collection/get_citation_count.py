from pymongo import MongoClient
import pandas as pd

# Gets the citation count from the metadata stored in the databse

client = MongoClient('mongodb://localhost:27017/')  
db = client['crossref_metadata']  
collection = db['articles_references']  

df = pd.read_csv('final_GR_data.csv')

def get_citation_count(doi):
    paper = collection.find_one({'DOI': doi})
    if paper and 'is-referenced-by-count' in paper:
        return paper['is-referenced-by-count']
    return 0 

df['Citation Count'] = df['DOI'].apply(get_citation_count)

updated_csv_path = 'final_updated_data.csv'
df.to_csv(updated_csv_path, index=False)

print(f"Updated data with citation counts saved to {updated_csv_path}")
