import re
import requests
from bs4 import BeautifulSoup
import gender_guesser.detector as gender
from name2nat import Name2nat


gender_detector = gender.Detector()
#natnat = Name2nat()

def get_doi(url):
    doi_pattern = re.compile(r'10.\d{4,9}/[-._;()/:A-Za-z0-9]+')
    doi_match = doi_pattern.search(url)
    if doi_match:
        return doi_match.group()
    try:
        response = requests.get(url, headers={'User-Agent': 'Gouled/0.1 (mailto:gouledmahamud@gmail.com)'})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            meta_tags = soup.find_all('meta', attrs={'name': re.compile(r'doi', re.I)})
            for tag in meta_tags:
                if 'content' in tag.attrs:
                    meta_doi_match = doi_pattern.search(tag.attrs['content'])
                    if meta_doi_match:
                        return meta_doi_match.group()
    except requests.RequestException:
        pass
    return None

def get_metadata(doi):
    base_url = "https://api.crossref.org/works/"
    headers = {'User-Agent': 'Gouled/0.1 (mailto:gouledmahamud@gmail.com)'}
    response = requests.get(base_url + doi, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def author_info(metadata):
    authors_info = []
    names = []
    if metadata and 'message' in metadata and 'author' in metadata['message']:
        for author in metadata['message']['author']:
            given_name = author.get('given', "")
            family_name = author.get('family', "")
            full_name = f"{given_name} {family_name}".strip()
            names.append(full_name)
    
    #nationalities = natnat(names, top_n=3)
    
    for i, author in enumerate(metadata['message']['author']):
        given_name = author.get('given', "")
        family_name = author.get('family', "")
        full_name = f"{given_name} {family_name}".strip()
        affiliation = author['affiliation'][0]['name'] if 'affiliation' in author and len(author['affiliation']) > 0 else "No affiliation found"
        first_name = given_name.split()[0] if given_name else ""
        gender = gender_detector.get_gender(first_name)
        
        #nationality = nationalities[i][1][0][0] if i < len(nationalities) else "Unknown"
        
        #authors_info.append({'name': full_name, 'affiliation': affiliation, 'gender': gender, 'nationality': nationality})
        authors_info.append({'name': full_name, 'affiliation': affiliation, 'gender': gender})
        
    return authors_info

if __name__ == "__main__":
    #article_url = "https://link.springer.com/article/10.1007/s10710-017-9314-z"
    article_url = "https://www.computer.org/csdl/journal/tp/2023/03/09826417/1EVdA0iYdFu"
    #doi = get_doi(article_url)
    doi = "10.1109/TPAMI.2022.3174724"
    if doi:
        metadata = get_metadata(doi)
        authors_info = author_info(metadata)
        
        for author in authors_info:
            #print(f"Author: {author['name']} | Affiliation: {author['affiliation']} | Gender: {author['gender'].title()} | Nationality: {author['nationality']}")
            print(f"Author: {author['name']} | Affiliation: {author['affiliation']} | Gender: {author['gender'].title()}")
    else:
        print("DOI could not be found.")
