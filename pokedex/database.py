import sqlite3



class Database:
    def __init__(self):
        self.conn = sqlite3.connect("pokedex.db")
        self.cur = self.conn.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS pokemon
            (id INTEGER PRIMARY KEY,
            number INTEGER,
            base_name TEXT,
            form_name TEXT,
            hp INTEGER,
            atk INTEGER,
            def INTEGER,
            spatk INTEGER,
            spdef INTEGER,
            speed INTEGER)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS pokemon_type_rel
            (id INTEGER PRIMARY KEY,
            pokemon_id INTEGER,
            type TEXT)""")
        self.conn.commit()

        self.cmd_insert_pkmn = """INSERT INTO pokemon
            (number, base_name, form_name, hp, atk,  def, spatk, spdef, speed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        self.cmd_insert_type = """INSERT INTO pokemon_type_rel
            (pokemon_id, type)
            VALUES (?, ?)"""
        self.cmd_query_numbers = """SELECT DISTINCT number FROM pokemon"""


    def close(self):
        self.conn.close()


    def insert(self, pokemon):
        # "pokemon" will be a tuple with these attributes:
        # pokemon[0] - National Pokedex number
        # pokemon[1] - name of base form
        # pokemon[2] - name of this form in particular
        # pokemon[3] - list of types as strings (either one or two)
        # pokemon[4] - list of stats (ordered: hp, atk, def, spatk, spdef, speed)

        result_msgs = []

        for i in range(len(pokemon[2])):
            ins = []
            ins += [pokemon[0], pokemon[1], pokemon[2][i]]
            ins += pokemon[4][i]

            self.cur.execute(self.cmd_insert_pkmn, ins)
            pokemon_id = self.cur.lastrowid

            types = pokemon[3][i]
            for t in types:
                self.cur.execute(self.cmd_insert_type, (pokemon_id, t))

            result_msgs.append("Added #" + str(pokemon[0]) + " " + pokemon[1] + " - Form: " + pokemon[2][i])

        self.conn.commit()
        for msg in result_msgs: print(msg)


    def find_numbers_added(self):
        numbers_added = []

        for result in self.cur.execute(self.cmd_query_numbers):
            numbers_added.append(result[0])

        return numbers_added
