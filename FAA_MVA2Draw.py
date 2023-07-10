from bs4 import BeautifulSoup
import json

with open("L30_LAS_MVA_2022.xml") as f:
    data = f.read()
    
root = BeautifulSoup(data, features="xml")

airspaces = root.find_all("ns3:geometryComponent")

output = []

for airspace in airspaces:
    #print(airspace.name)
    alt = int(airspace.AirspaceGeometryComponent.theAirspaceVolume.AirspaceVolume.minimumLimit.text.strip()[:-2])
    name = airspace.parent.find('name').text.strip()
    points = []
    try:
        outer_ring_str = airspace.AirspaceGeometryComponent.theAirspaceVolume.AirspaceVolume.horizontalProjection.Surface.patches.PolygonPatch.exterior.LinearRing.posList.text.strip().split()
        outer_ring_int = [[float(i) for i in outer_ring_str[s:s+2][::-1]] for s in range(0, len(outer_ring_str), 2)]
        print(outer_ring_int)
        points.extend(outer_ring_int)
    except:
        pass
    
    try:
        inner_ring_str = airspace.AirspaceGeometryComponent.theAirspaceVolume.AirspaceVolume.horizontalProjection.Surface.patches.PolygonPatch.interior.LinearRing.posList.text.strip().split()
        inner_ring_int = [[float(i) for i in outer_ring_str[s:s+2][::-1]] for s in range(0, len(inner_ring_str), 2)]
        print(inner_ring_int)
        points.extend(inner_ring_int)
    except:
        pass

    points = [x for x in points if len(x) == 2]
    print([[len(points[i]), name] for i in range(len(points))])

    output.append(
        {
            "author": "",
            "brushStyle": 1,
            "color": "#ff646464",
            "colorBg": "#00ff0000",
            "lineWidth": 2,
            "name": name,
            "points": [{"latitude": i[0], "longitude": i[1]} for i in points],
            "shared": False,
            "timestamp": "",
            "type": "polygon"
        }
    )

with open("KZLA_MVA.json", "w") as f:
    f.write(json.dumps({
        "author": "me",
        "drawings": output,
        "enable": "true",
        "name": "KSLV_MVA",
        "shared": False,
        "timestamp": "",
        "type": "layer"
    }))