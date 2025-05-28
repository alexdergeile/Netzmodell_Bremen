import pypsa

netz = pypsa.Network()
netz.set_snapshots(["2025-01-01 00:00"])

netz.add("Bus", "Bus1", v_nom=110)
netz.add("Bus", "Bus2", v_nom=110)

netz.add("Line", "Leitung", bus0="Bus1", bus1="Bus2", r=0.01, x=0.05, s_nom=100)

netz.add("Load", "Last", bus="Bus2", p_set=60)
netz.add("Generator", "Gen", bus="Bus1", p_set=60)

netz.lpf()

print("Leitungsfluss:")
print(netz.lines_t.p0)