# bulbapedia-pokedex-webscraper
Code for blog post about Python web scraping with BeautifulSoup and SQLite databases
You can find the blog post here: http://luca-wel.com.

### About
This script will go through pages of [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Main_Page)
and automatically write the following pieces of information for all Pokémon into a SQLite database:
* name and number in National Pokédex
* type(s)
* base stats
* all its alternative forms (e.g. Mega Evolution, Alolan forms, ...)

### Setup
You need to have Python 3 installed on your machine.
Furthermore, install these libraries using pip:
```
pip install requests bs4 html5lib
```

To create the database on your own run these commands:
```
python create-pokedex.py
python manual-insertions.py
```
Alternatively, use the already filled one from this repo.

### Usage
Example: Get the Sp.Atk base value of all _Deoxys_ forms:
```
SELECT form_name, spatk FROM pokemon WHERE base_name = "Deoxys"
```

Example: Find the pokemon with highest Def value.
```
SELECT base_name, form_name, MAX(atk) FROM pokemon
```

Example: Find all _Fire_ type pokemon.
```
SELECT base_name, form_name FROM pokemon
JOIN pokemon_type_rel
ON pokemon.id = pokemon_type_rel.pokemon_id
WHERE pokemon_type_rel.type = "Fire"
```

Example: Find all _Dragon_/_Flying_ type pokemon.
```
SELECT base_name, form_name FROM pokemon
JOIN pokemon_type_rel
ON pokemon.id = pokemon_type_rel.pokemon_id
WHERE pokemon_type_rel.type = "Dragon"

INTERSECT

SELECT base_name, form_name FROM pokemon
JOIN pokemon_type_rel
ON pokemon.id = pokemon_type_rel.pokemon_id
WHERE pokemon_type_rel.type = "Flying"
```
