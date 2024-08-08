# PokeMMO-NoMoLostShinies
A pokedex/shiny hunting helper in python for CLI

# Prerequisites
- Python 3.x
- Python libraries "colorama" and "tabulate" (there is a requirement.txt)

# Step by step setup

For the non-tech people, here's a simplified version : 
You need python, for that, you can just download the latest version from the Microsoft Store which is the version 3.12, but olders versions should be OK.
https://apps.microsoft.com/detail/9ncvdn91xzqp?hl=en-US&gl=US

Once you have Python installed, you need to download the ZIP file containing the tool, you can do it like this

![Alt text](assets/zip_dl.png)

Once you have the ZIP file, you can just extract it

![Alt text](assets/extract.png)

After that, go in the folder, right click in a blank space, select "Open in terminal"

![Alt text](assets/open_in_terminal.png)

Then you just have to copy paste the following command : 
```
pip install -r requirements.txt
```
Once it's done, everything is setup, you just have to launch the script with python as seen in the next part.

# Usage
Once you have clone the repository and downloaded the prerequisite (or pip install -r requirements.txt), you can just launch the script at the root of the folder like this 
```
python main.py
```

You will have to select the region you will be shiny hunting in ...

![Alt text](assets/selection.png)

... then the area.

![Alt text](assets/sinnoh_victory_road.png)

The table will show you every revelant data concerning the pokemons you will be able to encounter such as held items, lvl, type, rarity, ... as seen in the dex, like a reverse dex where you search by location instead of Pokemons.

But the true value is in the 4 last columns as they will indicate what risky moves, items or boring abilities the mon can have, based on his dex data.

Tips : Moves in violet are moves that the pokemon has learned, but should have replaced by other moves since.

The last column contains recommendations for every scenarios so you can get prepared and not risk a lost shiny that you didn't expected or didn't prepared well enough for.
It used the "recommendation.json" file to give custom countermeasure
![Alt text](assets/recommendations.png)

# Tips
I advise you to zoom out a bit on the terminal, so the table have enough space to be rendered properly, I'm going to work a bit on that later, or keep the change for the V2


# Roadmap
- V1 : V1 is a working script, with every risks taken in account, good logic, ...
- V2 : When I'll consider it finished, I'll port this to a webapp as a V2, maybe with wome React, so that way I can make it better at handling a table, use cards or else, adding the shiny sprites .gif, ...
- V3 : When I'll arrive at a V2 that is good enough, I'll probably move on to the V3 which will be a toast notification like the GEC is doing to integrate the script to the PokeMMO windows and have it automatically define the region you are in and the risk you can have, using OCR and Pygames is my idea for now and I have explored it already