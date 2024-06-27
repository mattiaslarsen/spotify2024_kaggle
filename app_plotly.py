import streamlit as st
import pandas as pd
import plotly.express as px

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
    
    # Interaktivt histogram över Track Score
    st.header("Interaktivt Histogram över Track Score")
    st.write("Histogrammet nedan visar fördelningen av Track Score för de mest streamade låtarna på Spotify under 2024.")
    fig = px.histogram(df, x='Track Score', nbins=20, title='Fördelning av Track Score')
    fig.update_layout(xaxis_title='Track Score', yaxis_title='Antal låtar')
    st.plotly_chart(fig)

    # Interaktiv boxplot för Track Score
    st.header("Boxplot för Track Score")
    st.write("Boxploten nedan visar spridningen av Track Score för de mest streamade låtarna på Spotify under 2024.")
    fig = px.box(df, y='Track Score', title='Boxplot för Track Score')
    fig.update_layout(yaxis_title='Track Score')
    st.plotly_chart(fig)

    # Interaktiv boxplot för Track Score per år
    st.header("Boxplot för Track Score per år")
    st.write("Boxploten nedan visar spridningen av Track Score för de mest streamade låtarna på Spotify under 2024, grupperade per år.")
    df['Year'] = df['Release Date'].dt.year  # Skapa en ny kolumn för år
    fig = px.box(df, x='Year', y='Track Score', title='Boxplot för Track Score per år')
    fig.update_layout(xaxis_title='År', yaxis_title='Track Score')
    st.plotly_chart(fig)

    # Interaktivt linjediagram över genomsnittligt Track Score per månad
    st.header("Genomsnittligt Track Score per månad")
    st.write("Linjediagrammet nedan visar den genomsnittliga Track Score per månad för de mest streamade låtarna på Spotify under 2024.")
    df['Month'] = df['Release Date'].dt.to_period('M').astype(str)
    monthly_avg_score = df.groupby('Month')['Track Score'].mean().reset_index()
    fig = px.line(monthly_avg_score, x='Month', y='Track Score', title='Genomsnittligt Track Score per månad')
    fig.update_layout(xaxis_title='Månad', yaxis_title='Genomsnittligt Track Score')
    st.plotly_chart(fig)


except Exception as e:
    # Hantera eventuella fel vid inläsning av CSV-filen
    st.error(f"Fel vid inläsning av CSV-fil: {e}")
