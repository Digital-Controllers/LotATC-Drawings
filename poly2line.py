import sys
import json

with open(sys.argv[1], "r") as f:
    input_obj = json.loads(f.read())
    
for draw in input_obj["drawings"]:
    draw["type"] = "line"
    draw["points"].append(draw["points"][0])
    
with open(sys.argv[2], "w") as f:
    f.write(json.dumps(input_obj))