import pypsa
import pandas as pd
from geopy.distance import distance

# Lastdaten laden
lastdaten = pd.read_csv(
    "Summenlastgang/Aufgeteilter_Summenlastgang.csv",
    parse_dates=["Zeit"],
    index_col="Zeit"
)

netz = pypsa.Network()
netz.set_snapshots(lastdaten.index)

# Koordinaten der Busse
knoten_koordinaten = {
    "Knoten_1": (53.14, 8.85),  # Bremen Nord
    "Knoten_2": (53.02, 8.80)   # Bremen Süd
}

# Busse mit Koordinaten
netz.add("Bus", "Knoten_1", v_nom=110, x=knoten_koordinaten["Knoten_1"][1], y=knoten_koordinaten["Knoten_1"][0])
netz.add("Bus", "Knoten_2", v_nom=110, x=knoten_koordinaten["Knoten_2"][1], y=knoten_koordinaten["Knoten_2"][0])

# Leitung
netz.add("Line", "Leitung_K1_K2",
         bus0="Knoten_1",
         bus1="Knoten_2",
         r=0.01,
         x=0.1,
         s_nom=1000)

# Lasten
netz.add("Load", "Last_K1", bus="Knoten_1", p_set=lastdaten["Last_Knoten_1"])
netz.add("Load", "Last_K2", bus="Knoten_2", p_set=lastdaten["Last_Knoten_2"])

# Slack-Generator
netz.add("Generator", "SlackGen", bus="Knoten_1", p_nom=1e6, control="Slack")

# Fiktive Generatoren mit Koordinaten
generatoren = [
    {"name": "Gen_A", "lat": 53.12, "lon": 8.84, "p_nom": 0.05},
    {"name": "Gen_B", "lat": 53.04, "lon": 8.81, "p_nom": 0.075},
    {"name": "Gen_C", "lat": 53.10, "lon": 8.83, "p_nom": 0.1}
]

# Funktion zur Knoten-Zuordnung per Entfernung
def nächstgelegener_knoten(lat, lon):
    return min(knoten_koordinaten.keys(),
               key=lambda k: distance((lat, lon), knoten_koordinaten[k]).km)

# Generatoren zuordnen und einfügen
for gen in generatoren:
    bus = nächstgelegener_knoten(gen["lat"], gen["lon"])
    netz.add("Generator", gen["name"], bus=bus, p_nom=gen["p_nom"], p_set=gen["p_nom"])

# Netzberechnung
netz.pf()

# leistungsfluss durch Leitung in csv
netz.lines_t.p0.to_csv("Ergebnisse/Leitungsfluss.csv")

# Generator-Leistungen in csv
netz.generators_t.p.to_csv("Ergebnisse/Generatorenleistung.csv")

print("\n Netzmodell erfolgreich berechnet!\n")
print("Leistungsfluss durch Leitung:")
print(netz.lines_t.p0.head())