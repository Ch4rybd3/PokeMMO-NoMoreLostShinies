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

def load_locations():
    with open("locations.json", 'r') as file:
        return json.load(file)

def load_pokemon_data(pokemon_id):
    filepath = os.path.join("pokemons", f"{pokemon_id}.json")
    with open(filepath, 'r') as file:
        return json.load(file)

def load_list(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def load_recommendations():
    with open("recommendation.json", 'r') as file:
        return json.load(file)

def normalize_location(location):
    return re.sub(r'\s*\(.*?\)', '', location).strip()

def get_recommendations(risky_moves, boring_abilities, risky_items, recommendation_data):
    recommendations = []

    if risky_moves:
        move_recommendations = [recommendation_data["risk_moves"].get(move.split(' (')[0].lower(), None) for move in risky_moves]
        move_recommendations = [rec for rec in move_recommendations if rec]  # Filter out None
        if move_recommendations:
            recommendations.append('\n'.join(move_recommendations))

    if boring_abilities:
        ability_recommendations = [recommendation_data["boring_abilities"].get(ability.lower(), None) for ability in boring_abilities]
        ability_recommendations = [rec for rec in ability_recommendations if rec]  # Filter out None
        if ability_recommendations:
            recommendations.append('\n'.join(ability_recommendations))

    if risky_items:
        item_recommendations = [recommendation_data["risky_items"].get(item.lower(), None) for item in risky_items]
        item_recommendations = [rec for rec in item_recommendations if rec]  # Filter out None
        if item_recommendations:
            recommendations.append('\n'.join(item_recommendations))

    return '\n'.join(recommendations) if recommendations else '-'

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_current_moveset(pokemon_moves, min_level, max_level):
    """Return the last 4 moves learned by the Pokémon up to min_level, plus all moves learned between min_level and max_level."""
    # Moves learned up to min_level
    moves_up_to_min_level = [move for move in pokemon_moves if 'level' in move and move['level'] <= min_level]
    moves_up_to_min_level.sort(key=lambda move: move['level'], reverse=True)
    last_moves_before_min_level = moves_up_to_min_level[:4]

    # Moves learned between min_level and max_level
    moves_between_levels = [move for move in pokemon_moves if 'level' in move and min_level < move['level'] <= max_level]
    moves_between_levels.sort(key=lambda move: move['level'])

    # Combine both lists
    combined_moveset = last_moves_before_min_level + moves_between_levels

    return combined_moveset

def main():
    locations = load_locations()
    recommendation_data = load_recommendations()

    # Load lists from JSON files
    risky_moves = load_list("risky_moves.json")
    boring_abilities = load_list("boring_abilities.json")
    risky_items = load_list("risky_items.json")
    
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

    # Clear terminal before displaying the table
    clear_terminal()
    
    print(f"Selected Region: {selected_region}")
    print(f"Selected Location: {selected_location}")
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
        max_level = location['max_level']
        min_level = location['min_level']

        # Get the current moveset for the Pokémon
        current_moveset = get_current_moveset(pokemon['moves'], min_level, max_level)

        # Collect risky moves based on max_level with level info
        risky_move_list = []
        for move in pokemon['moves']:
            if 'level' in move and move['name'].lower() in risky_moves:
                if max_level >= move['level']:
                    if move not in current_moveset:
                        # If the move is not in the current moveset, color it violet
                        risky_move_list.append(f"{Fore.MAGENTA}{move['name']} ({move['level']}){Style.RESET_ALL}")
                    else:
                        risky_move_list.append(f"{move['name']} ({move['level']})")

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

        recommendations = get_recommendations(risky_move_list, boring_ability_list, risky_item_list, recommendation_data)

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
            ', '.join(risky_item_list) if risky_item_list else '-',
            recommendations
        ]
        table_data.append(row)

    # Print the table
    headers = ["Nom", "ID", "Location type", "Rarity", "Minlvl - Maxlvl", "Held Item", "Day Time/Season", "Risk Move", "Boring Abilities", "Risky Items", "Recommendations"]
    print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()
