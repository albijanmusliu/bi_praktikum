import pandas as pd

# Load data
data = pd.read_tsv('C:\Users\TDGCBUF\Desktop\THI\4_Semester\BI_und_Datenanalyse\error_240410\title_basics.tsv')
# Split text into a list
data['genres'] = data['genres'].str.split(',')
# Convert list into multiple rows
data = data.explode('Skills')
print(data)