import pandas as pd
from geopy.distance import geodesic

# --- Pfade ---
generatoren_pfad = "/home/slatty/Uni/M.Sc/Master SEM III/Masterprojekt/PyPSA/Daten für Projekt/Generators.csv + einspeiseprofile/generators_aggregated.csv"
buses_pfad = "/home/slatty/Uni/M.Sc/Master SEM III/Masterprojekt/PyPSA/Daten für Projekt/Knoten+Leitungen (important)/pypsa_substations_110kV_filtered_cleaned.csv"
ausgabe_pfad = "/home/slatty/Uni/M.Sc/Master SEM III/Masterprojekt/PyPSA/Daten für Projekt/Generators.csv + einspeiseprofile/generators_with_bus.csv"

# --- CSVs laden ---
gen_df = pd.read_csv(generatoren_pfad)
bus_df = pd.read_csv(buses_pfad)


# --- Spalten korrekt umbenennen ---
bus_df.rename(columns={"x": "lon", "y": "lat", "name": "bus"}, inplace=True)


# --- Typ-Sicherheit ---
gen_df["lat"] = gen_df["lat"].astype(float)
gen_df["lon"] = gen_df["lon"].astype(float)
bus_df["lat"] = bus_df["lat"].astype(float)
bus_df["lon"] = bus_df["lon"].astype(float)


# --- Nächstgelegenen Bus finden ---
def finde_naechsten_bus(gen_koord, bus_df):
    min_dist = float("inf")
    naechster_bus = None
    for _, bus in bus_df.iterrows():
        dist = geodesic(gen_koord, (bus["lat"], bus["lon"])).meters
        if dist < min_dist:
            min_dist = dist
            naechster_bus = bus["bus"]
    return naechster_bus




# --- Berechnung ---
gen_df["bus"] = gen_df.apply(lambda row: finde_naechsten_bus((row["lat"], row["lon"]), bus_df), axis=1)

# --- Speichern ---
gen_df.to_csv(ausgabe_pfad, index=False)
print(f"Bus-Zuordnung abgeschlossen. Datei gespeichert unter:\n{ausgabe_pfad}") 