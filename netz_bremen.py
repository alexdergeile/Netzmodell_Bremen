import pypsa
import pandas as pd

# Lastdaten laden
lastdaten = pd.read_csv(
    "Summenlastgang/Aufgeteilter_Summenlastgang.csv",
    parse_dates=["Zeit"],
    index_col="Zeit"
)

# Netzwerk initialisieren
netz = pypsa.Network()

# Zeithorizont setzen
netz.set_snapshots(lastdaten.index)

# Zwei Hochspannungs-Busse hinzufügen
netz.add("Bus", "Knoten_1", v_nom=110)
netz.add("Bus", "Knoten_2", v_nom=110)

# Leitung zwischen den Knoten (geschätzt: 10 km, grobe technische Werte)
netz.add("Line", "Leitung_K1_K2",
         bus0="Knoten_1",
         bus1="Knoten_2",
         r=0.01,      # Ohm
         x=0.1,       # Reaktanz in Ohm
         s_nom=1000)  # Scheinleistung in MVA

# Last an beiden Knoten hinzufügen
netz.add("Load", "Last_K1", bus="Knoten_1", p_set=lastdaten["Last_Knoten_1"])
netz.add("Load", "Last_K2", bus="Knoten_2", p_set=lastdaten["Last_Knoten_2"])

# Slack-Generator am Knoten_1 zur Bilanzierung
netz.add("Generator", "SlackGen", bus="Knoten_1", p_nom=1e6, control="Slack")

# Nichtlinearer Lastfluss (AC) berechnen
netz.pf()

# Ergebnis anzeigen
print("\n Netzmodell erfolgreich berechnet!\n")
print("Leistungsfluss durch Leitung:")
print(netz.lines_t.p0.head())