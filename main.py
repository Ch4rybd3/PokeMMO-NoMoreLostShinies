import json
import os
import re
from colorama import Fore, Style, init
from tabulate import tabulate

# Initialize colorama
init()

# Define the custom order for rarities
rarity_order = [
    "Horde", "Very Common", "Common", "Uncommon", "Lure", "Rare", "Very Rare", "Special"
]

# Define the custom order for regions
region_order = [
    "Kanto", "Johto", "Hoenn", "Sinnoh", "Unova"
]

# Define risky moves
risky_moves = [
    "selfdestruct", "take down", "follow me", "rage powder", "trick", "transform", "memento", "perish song", "sketch", "curse", "grudge", "teleport", "destiny bond", "trash", "outrage", "final gambit", "double edge", "brave bird", "soak", "roar", "whirlwind", "ally switch", "petal dance", "teeter dance"
]

# Define boring abilities
boring_abilities = [
    "intimidate", "trace", "reactive gaze", "arena trap", "shadow tag", "forewarn", "illusion", "unnerve", "mold breaker"
]

# Define risky items
risky_items = [
    "iron barbs", "black sludge", "toxic orb", "life orb", "flame orb"
]

def load_locations():
    with open("locations.json", 'r') as file:
        return json.load(file)

def load_pokemon_data(pokemon_id):
    filepath = os.path.join("pokemons", f"{pokemon_id}.json")
    with open(filepath, 'r') as file:
        return json.load(file)

def normalize_location(location):
    return re.sub(r'\s*\(.*?\)', '', location).strip()

def main():
    locations = load_locations()
    
    print("Select a region:")
    regions = [region for region in region_order if region in locations]
    for idx, region in enumerate(regions, start=1):
        print(f"{idx}. {region}")

    region_choice = int(input("\nEnter region number: ")) - 1
    selected_region = regions[region_choice]

    print(f"\nLocations in {selected_region}:")
    locs = locations[selected_region]
    normalized_locs = list(set(normalize_location(loc) for loc in locs))
    normalized_locs.sort()

    for idx, loc in enumerate(normalized_locs, start=1):
        print(f"{idx}. {loc}")

    location_choice = int(input("\nEnter location number: ")) - 1
    selected_location = normalized_locs[location_choice]

    print(f"\nPokémon in {selected_location}:")

    encounters = []

    for filename in os.listdir("pokemons"):
        if filename.endswith(".json"):
            pokemon_data = load_pokemon_data(filename.split(".")[0])
            for location in pokemon_data.get("locations", []):
                if location["region_name"] == selected_region and normalize_location(location["location"]) == selected_location:
                    encounters.append((pokemon_data, location))
    
    # Sort encounters by rarity using the custom order
    encounters.sort(key=lambda x: rarity_order.index(x[1]["rarity"]))

    # Prepare data for table
    table_data = []
    for pokemon, location in encounters:
        # Collect risky moves based on max_level with level info
        risky_move_list = [
            f"{move['name']} ({move['level']})" for move in pokemon['moves']
            if 'level' in move and move['name'].lower() in risky_moves and location['max_level'] >= move['level']
        ]
        
        # Collect boring abilities
        boring_ability_list = [
            ability['name'].lower() for ability in pokemon['abilities']
            if ability['name'].lower() in boring_abilities
        ]
        
        # Collect risky items
        risky_item_list = [
            item['name'].lower() for item in pokemon['held_items']
            if item['name'].lower() in risky_items
        ]

        row = [
            pokemon['name'],
            pokemon['id'],
            location['type'],
            location['rarity'],
            f"{location['min_level']} - {location['max_level']}",
            ', '.join(item['name'] for item in pokemon['held_items']),
            location['location'].split('(', 1)[-1].rstrip(')') if '(' in location['location'] else '',
            ', '.join(risky_move_list) if risky_move_list else '-',
            ', '.join(boring_ability_list) if boring_ability_list else '-',
            ', '.join(risky_item_list) if risky_item_list else '-'
        ]
        table_data.append(row)

    # Print the table
    headers = ["Nom", "ID", "Location type", "Rarity", "Minlvl - Maxlvl", "Held Item", "Day Time/Season", "Risk Move", "Boring Abilities", "Risky Items"]
    print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()