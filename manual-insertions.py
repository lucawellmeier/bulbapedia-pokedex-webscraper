import sqlite3

conn = sqlite3.connect("pokedex.db")
cur = conn.cursor()

cmd1 = """INSERT INTO pokemon
            (number, base_name, form_name, hp, atk,  def, spatk, spdef, speed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
cmd2 = """INSERT INTO pokemon_type_rel
            (pokemon_id, type)
            VALUES (?, ?)"""


a = []
b = []


# 479 Rotom
# reason:
# - second line of forms is not parsed
# - two stat tables for 6 forms
a += [
    (479, "Rotom", "Rotom", 50, 50, 77, 95, 77, 91),
    (479, "Rotom", "Heat Rotom", 50, 65, 107, 105, 107, 86),
    (479, "Rotom", "Wash Rotom", 50, 65, 107, 105, 107, 86),
    (479, "Rotom", "Frost Rotom", 50, 65, 107, 105, 107, 86),
    (479, "Rotom", "Fan Rotom", 50, 65, 107, 105, 107, 86),
    (479, "Rotom", "Mow Rotom", 50, 65, 107, 105, 107, 86)
]
b += [
    ["Electric", "Ghost"],
    ["Electric", "Fire"],
    ["Electric", "Water"],
    ["Electric", "Ice"],
    ["Electric", "Flying"],
    ["Electric", "Grass"]
]


# 681 Aegislash
# reason: its forms are not mentioned in the header table
a += [
    (681, "Aegislash", "Shield Forme", 60, 50, 150, 50, 150, 60),
    (681, "Aegislash", "Blade Forme", 60, 150, 50, 150, 50, 60)
]
b += [
    ["Steel", "Ghost"],
    ["Steel", "Ghost"]
]


# 710 Pumpkaboo
# reason: its forms are not mentioned in the header table
a += [
    (710, "Pumpkaboo", "Small Size", 44, 66, 70, 44, 55, 56),
    (710, "Pumpkaboo", "Average Size", 49, 66, 70, 44, 55, 51),
    (710, "Pumpkaboo", "Large Size", 54, 66, 70, 44, 55, 46),
    (710, "Pumpkaboo", "Super Size", 59, 66, 70, 44, 55, 41)
]
b += [
    ["Ghost", "Grass"],
    ["Ghost", "Grass"],
    ["Ghost", "Grass"],
    ["Ghost", "Grass"]
]


# 711 Gourgeist
# reason: its forms are not mentioned in the header table
a += [
    (711, "Gourgeist", "Small Size", 55, 85, 122, 58, 75, 99),
    (711, "Gourgeist", "Average Size", 65, 90, 122, 58, 75, 84),
    (711, "Gourgeist", "Large Size", 75, 95, 122, 58, 75, 69),
    (711, "Gourgeist", "Super Size", 85, 100, 122, 58, 75, 41)
]
b += [
    ["Ghost", "Grass"],
    ["Ghost", "Grass"],
    ["Ghost", "Grass"],
    ["Ghost", "Grass"]
]


for i in range(len(a)):
    cur.execute(cmd1, a[i])
    pokemon_id = cur.lastrowid

    for t in b[i]:
        cur.execute(cmd2, (pokemon_id, t))

conn.commit()
conn.close()
