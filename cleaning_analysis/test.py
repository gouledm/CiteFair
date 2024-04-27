import pandas as pd

#Finds any missing fields

df = pd.read_csv('final_GR_data.csv')

rows_with_blanks = df.isna().any(axis=1).sum()

print(f"Number of rows with one or more blank cells: {rows_with_blanks}")
