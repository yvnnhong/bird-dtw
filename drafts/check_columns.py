from bird_dtw.species.arctic_tern.data import fetch_data

df = fetch_data()
print("organismID unique:", df['organismID'].nunique())
print(df['organismID'].unique())

print("catalogNumber unique:", df['catalogNumber'].nunique())
print("occurrenceID unique:", df['occurrenceID'].nunique())
print("recordNumber unique:", df['recordNumber'].nunique())