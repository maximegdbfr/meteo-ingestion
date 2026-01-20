import requests
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURATION ---
START_DATE = "2021-01-01"
END_DATE = "2024-01-01"
OUTPUT_DIR = "data/raw"
OUTPUT_FILE = "weather_history.parquet"

# Liste des villes avec leurs coordonnées (Lat/Lon)
CITIES = {
    "Paris": {"lat": 48.8566, "lon": 2.3522},
    "New_York": {"lat": 40.7128, "lon": -74.0060},
    "Tokyo": {"lat": 35.6762, "lon": 139.6503},
    "London": {"lat": 51.5074, "lon": -0.1278},
    "Sydney": {"lat": -33.8688, "lon": 151.2093}
}

def fetch_weather_data(city_name: str, lat: float, lon: float) -> pd.DataFrame:
    """
    Appelle l'API Open-Meteo pour une ville donnée et retourne un DataFrame.
    """
    url = "https://archive-api.open-meteo.com/v1/archive"
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "hourly": "temperature_2m,precipitation,wind_speed_10m,relative_humidity_2m",
        "timezone": "auto"
    }

    print(f"📡 Récupération des données pour {city_name}...")
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Erreur API ({response.status_code}): {response.text}")

    data = response.json()
    
    # Transformation du JSON en DataFrame Pandas
    hourly_data = data["hourly"]
    df = pd.DataFrame(hourly_data)
    
    # Ajout de métadonnées
    df["city"] = city_name
    df["ingested_at"] = datetime.now()
    
    return df

def main():
    """
    Fonction principale : Boucle sur les villes, consolide les données et sauvegarde en Parquet.
    """
    all_dfs = []

    # 1. Extraction (Extract)
    for city, coords in CITIES.items():
        try:
            df_city = fetch_weather_data(city, coords["lat"], coords["lon"])
            all_dfs.append(df_city)
        except Exception as e:
            print(f"❌ Erreur pour {city}: {e}")

    # 2. Consolidation
    if all_dfs:
        full_df = pd.concat(all_dfs, ignore_index=True)
        
        # S'assurer que le dossier existe
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # 3. Chargement (Load) -> Sauvegarde en Parquet
        output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
        
        # On utilise la compression 'snappy' (standard Big Data)
        full_df.to_parquet(output_path, index=False, compression='snappy')
        
        print(f"\n✅ Succès ! {len(full_df)} lignes ingérées.")
        print(f"📂 Fichier sauvegardé ici : {output_path}")
        
        # Petit aperçu pour le debug
        print("\n--- Aperçu des données ---")
        print(full_df.head())
    else:
        print("⚠️ Aucune donnée récupérée.")

if __name__ == "__main__":
    main()