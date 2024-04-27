import csv
import requests

#Retrieves the authors' names from crossref
# however, later on I decided to store the entire metadase for each DOI in a database
# otherwise I would be sending crossref too many requests

def fetch_authors_from_crossref(doi):
    url = f"https://api.crossref.org/works/{doi}"
    headers = {
        'User-Agent': 'youremail@gmail.com'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        data = response.json()
        authors = data['message'].get('author', [])
        author_names = ', '.join([f"{author.get('given')} {author.get('family')}" for author in authors if 'given' in author and 'family' in author])
        return author_names
    except requests.RequestException as e:
        print(f"Failed to fetch data for DOI {doi}: {e}")
        return None

def process_dois_and_fetch_authors(input_csv, output_csv):
    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=['DOI', 'Author'])
        writer.writeheader()

        for row in reader:
            doi = row['DOI'].strip()
            authors = fetch_authors_from_crossref(doi)
            if authors:
                writer.writerow({'DOI': doi, 'Author': authors})

if __name__ == "__main__":
    input_csv = 'dois.csv' 
    output_csv = 'output.csv' 
    process_dois_and_fetch_authors(input_csv, output_csv)
    print("Author details have been written to", output_csv)

