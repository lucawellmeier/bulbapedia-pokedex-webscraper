from pokedex.database import Database
from pokedex.webscraper import pokemon_info_generator


db = Database()
numbers_added = db.find_numbers_added()

for pokemon in pokemon_info_generator(numbers_added):
    db.insert(pokemon)

db.close()
