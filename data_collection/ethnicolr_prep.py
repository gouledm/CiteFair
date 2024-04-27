import pandas as pd

# Script to split author names into last name and first name columns
# because ethnicolr's webapp tool (I could not get it working locally) only accepts CSVs in that format

df = pd.read_csv('author_genders.csv')  

df_first_author = df['First Author'].str.split(' ', n=1, expand=True)
df_first_author.columns = ['first_name', 'last_name']
df_first_author = df_first_author[['last_name', 'first_name']]

df_last_author = df['Last Author'].str.split(' ', n=1, expand=True)
df_last_author.columns = ['first_name', 'last_name']
df_last_author = df_last_author[['last_name', 'first_name']]

df_first_author.to_csv('first_authors_names.csv', index=False)
df_last_author.to_csv('last_authors_names.csv', index=False)

print("CSV files for first and last authors' names have been created, with 'last_name' first.")
