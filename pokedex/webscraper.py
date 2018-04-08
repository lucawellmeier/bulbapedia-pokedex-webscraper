import requests
import bs4



def pokemon_info_generator(numbers_added):
    errors = []

    for number, base_name, details_url in _get_all_pokemon_base_entries():
        if number in numbers_added:
            print("Skipping #" + str(number) + " " + base_name + ": already added")
            continue

        #try:
        form_names, all_types, all_stats = _parse_pokemon_details(details_url, base_name)
        numbers_added.append(number)
        yield (number, base_name, form_names, all_types, all_stats)
        #except:
        #    print("Error parsing #" + str(number) + " " + base_name + ": manual handling needed")
        #    errors.append(number)
        #    continue

    print("Process finished")
    print("----------------")
    print("Manual handling needed for " + str(len(errors)) + " items")
    for error in errors:
        print(error, end=" ")




def _get_all_pokemon_base_entries():
    base_page_url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
    base_page_content = requests.get(base_page_url).content
    root = bs4.BeautifulSoup(base_page_content, "html5lib").find(id="mw-content-text")

    pokemon_base_entries = []
    generation_table_tags = root.find_all("table")[1:8]

    for gen_table_tag in generation_table_tags:
        pokemon_tr_tags = gen_table_tag.find("tbody").find_all("tr")[1:]

        for tr_tag in pokemon_tr_tags:
            pokemon_base_entries.append(_parse_pokemon_base_info(tr_tag))

    return pokemon_base_entries


def _parse_pokemon_base_info(tr_tag):
    cols = tr_tag.find_all("td", recursive=False)

    number = int(cols[1].string.replace(" ", "")[1:-1])

    details_link_tag = cols[3].find_all("a", recursive=False)[0]
    details_url = "https://bulbapedia.bulbagarden.net" + details_link_tag["href"]

    base_name = details_link_tag.string

    return number, base_name, details_url


def _parse_pokemon_details(details_page_url, base_name):
    details_page = requests.get(details_page_url)
    soup = bs4.BeautifulSoup(details_page.content, "html5lib")
    root = soup.find(id="mw-content-text")

    form_names = _parse_pokemon_forms(root, base_name)
    all_types = _parse_pokemon_types(root)
    all_stats = _parse_pokemon_stats(root, form_names)

    return form_names, all_types, all_stats


def _parse_pokemon_forms(root, base_name):
    form_names = []

    # navigate to the description table
    soup = root.find_all("table", recursive=False)[1].find("tbody")
    soup = soup.find("tr").find("td").find("table").find("tbody")
    soup = soup.find_all("tr", recursive=False)[1].find("td")
    soup = soup.find("table").find("tbody").find_all("tr", recursive=False)

    # memorize the names of the different forms
    combined_forms = soup[0].find_all("td", recursive=False) + soup[1].find_all("td", recursive=False)
    for s in combined_forms:
        s = s.find_all("small", recursive=False)
        if len(s) > 0:
            form_names.append(s[0].string)

    # if no special forms are found there won't be a name either;
    # add the base_name as form name in that case
    if len(form_names) == 0:
        form_names.append(base_name)

    return form_names


def _parse_pokemon_types(root):
    all_types = []

    # navigate to the section of containing table
    soup = root.find_all("table", recursive=False)[1].find("tbody")
    soup = soup.find_all("tr", recursive=False)[1].find("td")
    soup = soup.find("table").find("tbody").find("tr")
    soup = soup.find_all("td", recursive=False)

    # find all <table> tags
    type_tables = []
    for td in soup:
        if "style" in td.attrs:
            if "display" not in td["style"]:
                type_tables.append(td)
        else:
            type_tables.append(td)

    # add them to the list in the same order that the form names
    # have been parsed in
    for type_table in type_tables:
        types = []
        soup = type_table.find_all("td")

        for td in soup:
            if "style" not in td.attrs or "display" not in td["style"]:
                typeStr = td.find("a").find("span").find("b")
                types.append(typeStr.string)

        all_types.append(types)

    return all_types


def _parse_pokemon_stats(root, form_names):
    all_stats = []

    # load all table tags that contain actual stat data
    # -> load until you reach a table layout that is unlikely to be a stats table
    soup = root.find(id="Stats")
    if soup == None:
        soup = root.find(id="Base_stats")
    soup = soup.parent

    raw_stat_tables = []

    for table in soup.find_next_siblings("table"):
        rows = table.find("tbody").find_all("tr", recursive=False)
        if len(rows) != 10:
            break

        raw_stat_tables.append(table)

    # combine all sucessive tags with "Generation" in tag name (e.g.
    # "Generation I - V", "Generation VI onward") and add the last one of
    # them to the list (the current stats)
    filtered_stat_tables = []

    gen_in_name = False
    last_table = None

    for table in raw_stat_tables:
        table_desc = table.previous_sibling.previous_sibling.string

        if gen_in_name:
            if "Generation" not in table_desc:
                gen_in_name = False
                filtered_stat_tables.append(last_table)
                filtered_stat_tables.append(table)
            else:
                last_table = table
        else:
            if "Generation" not in table_desc:
                filtered_stat_tables.append(table)
            else:
                gen_in_name = True
                last_table = table

    if gen_in_name: # append last table if last stat table had "Generation" in name
        filtered_stat_tables.append(last_table)

    # now compare form_names with filtered_stat_tables and try to find
    # logical mapping
    mapped_stat_tables = []

    if len(filtered_stat_tables) == 1:
        for form in form_names:
            mapped_stat_tables.append(filtered_stat_tables[0])
    elif len(filtered_stat_tables) == len(form_names):
        mapped_stat_tables = filtered_stat_tables
    else:
        raise Exception("stats incompatible with forms")
        print("forms", len(form_names))
        print("raw stat tables", len(raw_stat_tables))
        print("filtered stat tables", len(filtered_stat_tables))

    # convert table to actual stat data
    for i in range(len(mapped_stat_tables)):
        single_stats = []
        rows = mapped_stat_tables[i].find("tbody").find_all("tr", recursive=False)
        for j in range(2, 8):
            soup = rows[j].find("td").find("table").find("tbody").find("tr")
            soup = soup.find_all("th", recursive=False)
            single_stats.append(int(soup[1].string))
        all_stats.append(single_stats)

    return all_stats
