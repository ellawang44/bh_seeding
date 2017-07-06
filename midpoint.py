import read

def preimage(key, galaxy):
    # get previous galaxies that are the pre image of the input galaxy
    keys = read.list_of_keys
    if key == keys[-1]:
        return []
    else:
        galaxies = [prev_galaxy for prev_galaxy in read.galaxy_data[keys[keys.index(key)+1]] if galaxy[0] == prev_galaxy[1]]
        return galaxies

def evolution(key, galaxy):
    # traces the evolution of 1 galaxy only. It will return a list of tuples where each tuple describes the galaxy at a different snapshot in reverse chronological order
    # I mean technically could've been written only to work for the present day snapshot galaxies, it would've been easier, but that's no fun c:
    # traces the biggest galaxy if a merger occurs
    keys = read.list_of_keys
    # set initial condition
    galaxy_list = [(key, galaxy)]
    current_galaxy = galaxy
    # a list of keys that come after the given key in the list
    next_keys = keys[-(len(keys) - keys.index(key)):]
    for current_key in next_keys:
        galaxies = preimage(current_key, current_galaxy)
        if len(galaxies) == 0:
            break
        elif len(galaxies) == 1:
            galaxy_list.append((current_key, galaxies[0]))
        else:
            galaxies = [g for g in galaxies if g[0] == current_galaxy[2]]
            galaxy_list.append(galaxies[0])
        current_key = keys[keys.index(current_key) + 1]
        current_galaxy = galaxies[0]
    return galaxy_list
