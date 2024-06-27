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
    
    # Förbättrat histogram över Track Score
    st.header("Histogram över Track Score")
    st.write("Histogrammet nedan visar fördelningen av Track Score för de mest streamade låtarna på Spotify under 2024.")
    fig, ax = plt.subplots()
    ax.hist(df['Track Score'], bins=20, edgecolor='black', color='skyblue')
    ax.set_xlabel('Track Score')
    ax.set_ylabel('Antal låtar')
    ax.set_title('Fördelning av Track Score')
    st.pyplot(fig)
    
    # Förbättrat linjediagram över genomsnittligt Track Score per månad
    st.header("Genomsnittligt Track Score per månad")
    st.write("Linjediagrammet nedan visar den genomsnittliga Track Score per månad för de mest streamade låtarna på Spotify under 2024.")
    df['Month'] = df['Release Date'].dt.to_period('M')
    monthly_avg_score = df.groupby('Month')['Track Score'].mean()
    fig, ax = plt.subplots()
    ax.plot(monthly_avg_score.index.astype(str), monthly_avg_score.values, color='green')
    ax.set_xlabel('Månad')
    ax.set_ylabel('Genomsnittligt Track Score')
    ax.set_title('Genomsnittligt Track Score per månad')
    plt.xticks(rotation=90)
    st.pyplot(fig)
    
    # Bubbeldiagram över Track Score vs Spotify Streams med Spotify Playlist Count som bubbla
    st.header("Track Score vs Spotify Streams med Spotify Playlist Count som bubbla")
    st.write("Bubbeldiagrammet nedan visar förhållandet mellan Track Score och Spotify Streams, där bubblornas storlek representerar Spotify Playlist Count.")
    fig, ax = plt.subplots()
    bubble_size = df['Spotify Playlist Count'] / 1000  # Justera bubbla storlek
    ax.scatter(df['Spotify Streams'], df['Track Score'], s=bubble_size, alpha=0.5, color='purple')
    ax.set_xlabel('Spotify Streams')
    ax.set_ylabel('Track Score')
    ax.set_title('Track Score vs Spotify Streams med Spotify Playlist Count som bubbla')
    st.pyplot(fig)
    
    # Boxplot för Track Score
    st.header("Boxplot för Track Score")
    st.write("Boxploten nedan visar spridningen av Track Score för de mest streamade låtarna på Spotify under 2024.")
    fig, ax = plt.subplots()
    ax.boxplot(df['Track Score'], vert=False)
    ax.set_xlabel('Track Score')
    ax.set_title('Boxplot för Track Score')
    st.pyplot(fig)

except Exception as e:
    # Hantera eventuella fel vid inläsning av CSV-filen
    st.error(f"Fel vid inläsning av CSV-fil: {e}")
