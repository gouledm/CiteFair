import os
import re
import csv

#Searches for and extracts DOIs from citation lists downloaded from IEEE 

def find_doi_column(header):
    for i, column_name in enumerate(header):
        if 'doi' in column_name.lower():
            return i
    return None  

def extract_dois_from_file(file_path):
    dois = set()
    if file_path.endswith('.csv'):
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader, None) 
            doi_index = find_doi_column(header)  
            if doi_index is None:
                print(f"No DOI column found in {file_path}")
                return list(dois)
            for row in reader:
                if row and len(row) > doi_index:
                    doi = row[doi_index].strip()
                    if doi:
                        dois.add(doi)
    else:
        doi_pattern = re.compile(r'\b10.\d{4,9}/[-._;()/:A-Z0-9]+\b', re.IGNORECASE)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            dois.update(doi_pattern.findall(content))
    return list(dois)

def read_existing_dois(csv_file):
    existing_dois = set()
    if os.path.isfile(csv_file):
        with open(csv_file, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  
            for row in reader:
                if row:
                    existing_dois.add(row[0].strip())
    return existing_dois

def write_dois_to_csv(dois, csv_file, existing_dois):
    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not os.path.isfile(csv_file) or os.path.getsize(csv_file) == 0:
            writer.writerow(['DOI']) 
        for doi in dois:
            if doi and doi not in existing_dois:
                writer.writerow([doi])
                existing_dois.add(doi)  

def process_directory(directory, csv_file):
    existing_dois = read_existing_dois(csv_file)
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename.endswith(".txt") or filename.endswith(".csv"):
            dois = extract_dois_from_file(file_path)
            write_dois_to_csv(dois, csv_file, existing_dois)

if __name__ == "__main__":
    # folder of dozens of txt files containing MLA/APA formatted citations
    directory = 'Documents/citations' 
    csv_file = 'dois.csv' 
    process_directory(directory, csv_file)
    print("Updated metadata has been written to", csv_file)
