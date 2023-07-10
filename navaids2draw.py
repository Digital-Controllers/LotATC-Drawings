import sqlite3
import json

FIR = "URRV"

con = sqlite3.connect("little_navmap_navigraph.sqlite")
cur = con.cursor()
data = cur.execute(f"SELECT * FROM waypoint WHERE laty > 40 AND laty < 46 AND lonx > 36 AND lonx < 46 AND region='{FIR[:2]}';").fetchall()
names = [des[0] for des in cur.description]


wps = []

for row in data:
    if any(char.isdigit() for char in row[3]):
        continue
    wpt = {
        "author": "",
        "brushStyle": 1,
        "color": "#ff646464",
        "colorBg": "#ff646464",
        "font": {
            "color": "#ff646464",
            "font": "Lato"
        },
        "lineWidth": 5,
        "shared": False,
        "timestamp": "",
        "type": "point"
    }
    
    wpt["name"] = row[3]
    wpt["text"] = row[3]
    wpt["latitude"] = float(row[-1])
    wpt["longitude"] = float(row[-2])
    wps.append(wpt)
    

final = {
    "author": "me",
    "drawings": wps,
    "enable": True,
    "name": f"{FIR}_NAVAIDS",
    "shared": False,
    "timestamp": "",
    "type": "layer",
    "visible": True
}

print(len(wps))

with open(f"{FIR}.json", "w") as f:
    f.write(json.dumps(final, indent=4))