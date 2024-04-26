import pandas as pd

# Load data
data = pd.read_csv(r'C:\Users\TDGCBUF\Desktop\THI\4_Semester\BI_und_Datenanalyse\error_240410\title.basics.tsv', sep=';', header=0)
#data = pd.read_csv(r'C:\Users\TDGCBUF\Desktop\albi.csv')

# Split text into a list
data['genres'] = data['genres'].str.split(',')
# Convert list into multiple rows
data = data.explode('genres')
print(data.head())