import os
import json

def gather_locations():
    pokemons_folder = "pokemons"
    locations = {}

    for filename in os.listdir(pokemons_folder):
        if filename.endswith(".json"):
            filepath = os.path.join(pokemons_folder, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                for location in data.get("locations", []):
                    region_name = location["region_name"]
                    loc_name = location["location"]
                    if region_name not in locations:
                        locations[region_name] = set()
                    locations[region_name].add(loc_name)

    # Convert sets to lists for JSON serialization
    for region in locations:
        locations[region] = list(locations[region])

    with open("locations.json", 'w') as outfile:
        json.dump(locations, outfile, indent=4)

if __name__ == "__main__":
    gather_locations()
