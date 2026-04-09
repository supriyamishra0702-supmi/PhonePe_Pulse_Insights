import requests

# Download the official India GeoJSON
url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
data = requests.get(url).json()

# Save it as a local file
with open('india_states.json', 'w') as f:
    import json
    json.dump(data, f)

print("✅ India map saved locally as 'india_states.json'!")

