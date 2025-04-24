import folium
import psycopg2
import json
import webbrowser
import os

# Parametry połączenia do bazy danych
db_params = {
    "dbname": "indoor_space",
    "user": "postgres",
    "password": "Test123!",
    "host": "localhost",
    "port": "5432"
}

# Połącz się z bazą danych PostgreSQL
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Wykonaj zapytanie SQL, aby pobrać dane z tabeli "person" (kolumna "position" typu geometry(Point, 2180)),
# transformując współrzędne z EPSG:2180 do EPSG:4326
cursor.execute("""
    SELECT ST_AsGeoJSON(ST_Transform(position, 4326)) FROM person;
""")

# Pobierz wyniki zapytania
rows = cursor.fetchall()

# Przekształć dane z wyników zapytania do formatu GeoJSON
features = []
for row in rows:
    if row[0] is not None:  # Sprawdź, czy `row[0]` nie jest None
        try:
            geojson = json.loads(row[0])  # `ST_AsGeoJSON` zwraca dane jako JSON
            # Bezpośrednio dodajemy 'type' i 'coordinates' do features
            features.append({
                "type": "Feature",
                "geometry": geojson,  # 'geojson' zawiera całą geometrię
                "properties": {}  # Możesz dodać tutaj dodatkowe właściwości, jeśli chcesz
            })
        except json.JSONDecodeError as e:
            print(f"Błąd podczas parsowania JSON: {e}")

# Zamknij połączenie z bazą danych
cursor.close()
conn.close()

# Utwórz GeoJSON FeatureCollection
geojson_data = {
    "type": "FeatureCollection",
    "features": features
}

# Utwórz mapę w centrum Warszawy (koordynaty lat, lon)
m = folium.Map(location=[52.2297, 21.0122], zoom_start=12)

# Dodaj dane GeoJSON na mapę
folium.GeoJson(geojson_data).add_to(m)

# Zapisz mapę do pliku HTML
map_path="map.html"
m.save(map_path)
webbrowser.open('file://' + os.path.realpath(map_path))
