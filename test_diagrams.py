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
    
    # Visa de första 10 raderna av datan
    st.header("De första 10 raderna av databasen")
    st.dataframe(df.head(10))
    
    # Visa de sista 10 raderna av datan
    st.header("De sista 10 raderna av databasen")
    st.dataframe(df.tail(10))
    
    # Konvertera 'Spotify Streams' och 'YouTube Views' till numeriska värden
    df['Spotify Streams'] = df['Spotify Streams'].str.replace(',', '').astype(float)
    df['YouTube Views'] = df['YouTube Views'].str.replace(',', '').astype(float)
    
    # Filtrera och visa de 10 mest streamade låtarna på Spotify
    top_songs_spotify = df.nlargest(10, 'Spotify Streams')[['Track', 'Spotify Streams', 'YouTube Views']]
    
    # Skapa ett stapeldiagram för Spotify Streams
    st.header("Top 10 mest streamade låtar på Spotify")
    fig, ax = plt.subplots()
    ax.barh(top_songs_spotify['Track'], top_songs_spotify['Spotify Streams'], color='blue')
    ax.set_xlabel('Spotify Streams')
    ax.set_title('Top 10 mest streamade låtar på Spotify')
    st.pyplot(fig)
    
    # Skapa ett stapeldiagram för YouTube Views
    st.header("Top 10 mest visade låtar på YouTube")
    fig, ax = plt.subplots()
    ax.barh(top_songs_spotify['Track'], top_songs_spotify['YouTube Views'], color='red')
    ax.set_xlabel('YouTube Views')
    ax.set_title('Top 10 mest visade låtar på YouTube')
    st.pyplot(fig)

except Exception as e:
    st.error(f"Fel vid inläsning av CSV-fil: {e}")
