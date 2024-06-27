import streamlit as st
import pandas as pd

# Sätt titeln på Streamlit-appen
st.title("Data Visualisering - Spotify Songs")

# Ange relativ sökväg till CSV-filen
csv_file = 'Most Streamed Spotify Songs 2024.csv'

# Försök att läsa in data från CSV-filen med 'latin1' teckenkodning
try:
    df = pd.read_csv(csv_file, encoding='latin1')
    st.write("CSV-filen har laddats framgångsrikt")
    st.dataframe(df.head(10))
except Exception as e:
    st.error(f"Fel vid inläsning av CSV-fil: {e}")
