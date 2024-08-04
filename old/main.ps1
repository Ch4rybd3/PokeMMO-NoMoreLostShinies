# Check if PSReadLine module is already loaded
if (-not (Get-Module -ListAvailable -Name PSReadLine)) {
    Import-Module PSReadLine
}

# Define the custom order for rarities
$rarity_order = @(
    "Horde",
    "Very Common",
    "Common",
    "Uncommon",
    "Lure",
    "Rare",
    "Very Rare",
    "Special"
)

# Define the custom order for regions
$region_order = @(
    "Kanto",
    "Johto",
    "Hoenn",
    "Sinnoh",
    "Unova"
)

function Load-Locations {
    return Get-Content -Path "locations.json" -Encoding UTF8 | ConvertFrom-Json
}

function Load-PokemonData {
    param (
        [string]$pokemonId
    )
    $filepath = Join-Path -Path "pokemons" -ChildPath "$pokemonId.json"
    return Get-Content -Path $filepath -Encoding UTF8 | ConvertFrom-Json
}

function Normalize-Location {
    param (
        [string]$location
    )
    return $location -replace '\s*\(.*?\)', '' -replace '\s+', ''
}

function Main {
    $locations = Load-Locations

    Write-Host "Select a region:"
    $regions = $region_order | Where-Object { $locations.PSObject.Properties.Name -contains $_ }
    for ($i = 0; $i -lt $regions.Count; $i++) {
        Write-Host "$($i + 1). $($regions[$i])"
    }

    $region_choice = [int](Read-Host "Enter region number") - 1
    $selected_region = $regions[$region_choice]

    Write-Host "Locations in $($selected_region):"
    $locs = $locations.$selected_region
    $normalized_locs = $locs | ForEach-Object { Normalize-Location $_ } | Select-Object -Unique | Sort-Object

    for ($i = 0; $i -lt $normalized_locs.Count; $i++) {
        Write-Host "$($i + 1). $($normalized_locs[$i])"
    }

    $location_choice = [int](Read-Host "Enter location number") - 1
    $selected_location = $normalized_locs[$location_choice]

    Write-Host "Pokémon in $($selected_location):"

    $encounters = @()

    Get-ChildItem -Path "pokemons" -Filter "*.json" | ForEach-Object {
        $pokemon_data = Load-PokemonData -pokemonId $_.BaseName
        foreach ($location in $pokemon_data.locations) {
            $normalized_loc = Normalize-Location $location.location
            if ($location.region_name -eq $selected_region -and $normalized_loc -eq $selected_location) {
                $encounters += @($pokemon_data, $location)
            }
        }
    }

    # Sort encounters by rarity using the custom order
    $encounters = $encounters | Sort-Object { $rarity_order.IndexOf($_[1].rarity) }

    # Prepare data for table
    $table_data = @()
    foreach ($encounter in $encounters) {
        $pokemon = $encounter[0]
        $location = $encounter[1]

        # Ensure the held items are correctly extracted
        $held_items = if ($pokemon.held_items) { 
            ($pokemon.held_items | ForEach-Object { $_.name }) -join ', ' 
        } else { 
            "None" 
        }
        
        # Extract the day time/season
        $day_time_season = if ($location.location -match '\((.*)\)') { 
            $matches[1] 
        } else { 
            '' 
        }

        # Detailed debugging output to check the $location variable
        Write-Host "DEBUG: Pokemon ID: $($pokemon.id), Name: $($pokemon.name)"
        Write-Host "DEBUG: Location Data: $($location | ConvertTo-Json -Depth 2)"

        # Create the row for the table
        $row = [PSCustomObject]@{
            "Nom"               = $pokemon.name
            "ID"                = $pokemon.id
            "Location type"     = $location.type
            "Rarity"            = $location.rarity
            "Minlvl - Maxlvl"   = "$($location.min_level) - $($location.max_level)"
            "Held Item"         = $held_items
            "Day Time/Season"   = $day_time_season
        }
        $table_data += $row
    }

    # Print the table
    if ($table_data.Count -eq 0) {
        Write-Host "No Pokémon found in the selected location."
    } else {
        $table_data | Format-Table -AutoSize
    }
}

Main
