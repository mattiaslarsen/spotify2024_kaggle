import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sätt titeln på Streamlit-appen
st.title("Most Streamed Spotify Songs 2024")

# Ange relativ sökväg till CSV-filen
csv_file = 'Most Streamed Spotify Songs 2024.csv'

# Försök att läsa in data från CSV-filen med 'latin1' teckenkodning
try:
    df = pd.read_csv(csv_file, encoding='latin1')
    st.write("CSV-filen har laddats framgångsrikt")
    
    # Funktion för att ta bort kommatecken och konvertera till heltal
    def clean_numeric_column(df, column):
        df[column] = df[column].str.replace(',', '').astype(float)
    
    # Kolumner att tvätta
    columns_to_clean = [
        'Spotify Streams', 'Spotify Playlist Count', 'Spotify Playlist Reach', 
        'YouTube Views', 'YouTube Likes', 'TikTok Posts', 'TikTok Likes', 
        'TikTok Views', 'YouTube Playlist Reach', 'Pandora Streams', 
        'Soundcloud Streams', 'Shazam Counts'
    ]
    
    # Applicera tvättfunktionen på kolumnerna
    for column in columns_to_clean:
        clean_numeric_column(df, column)
    
    # Konvertera övriga numeriska kolumner
    numeric_columns = [
        'All Time Rank', 'Track Score', 'Spotify Popularity', 
        'Apple Music Playlist Count', 'AirPlay Spins', 'SiriusXM Spins', 
        'Deezer Playlist Count', 'Deezer Playlist Reach', 'Amazon Playlist Count', 
        'Pandora Track Stations', 'TIDAL Popularity', 'Explicit Track'
    ]
    
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    
    # Konvertera Release Date till datumformat
    df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')
    
    # Hantera null-värden
    df['Artist'].fillna('Unknown', inplace=True)
    for column in columns_to_clean + numeric_columns:
        # Välj mellan median och medelvärde
        df[column].fillna(df[column].median(), inplace=True)  # Eller använd df[column].mean()
    
    # Visa de första 10 och sista 10 raderna för att kontrollera datatvätten
    st.write("Första 10 raderna:")
    st.dataframe(df.head(10))
    
    st.write("Sista 10 raderna:")
    st.dataframe(df.tail(10))

except Exception as e:
    # Hantera eventuella fel vid inläsning av CSV-filen
    st.error(f"Fel vid inläsning av CSV-fil: {e}")
