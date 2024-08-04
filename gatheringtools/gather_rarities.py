import os
import json

def gather_rarities():
    pokemons_folder = "pokemons"
    rarities = set()

    for filename in os.listdir(pokemons_folder):
        if filename.endswith(".json"):
            filepath = os.path.join(pokemons_folder, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                for location in data.get("locations", []):
                    rarity = location["rarity"]
                    rarities.add(rarity)

    # Convert the set to a list for JSON serialization
    rarities_list = list(rarities)

    with open("rarities.json", 'w') as outfile:
        json.dump(rarities_list, outfile, indent=4)

if __name__ == "__main__":
    gather_rarities()
