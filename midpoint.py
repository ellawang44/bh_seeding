import read

def m_preimage(key, galaxy):
    # get the biggest galaxy in te preimage of the input galaxy
    keys = read.list_of_keys
    if key == keys[-1]:
        return None
    else:
        prev_galaxy = [prev_galaxy for prev_galaxy in read.galaxy_data[keys[keys.index(key)+1]] if galaxy.previous == prev_galaxy.current]
        if prev_galaxy == []:
            return None
        else:
            return prev_galaxy[0]

def m_evolution(key, galaxy, threshold, var):
    # traces the evolution of 1 galaxy only. It will return a list of tuples where each tuple describes the galaxy at a different snapshot in reverse chronological order
    # I mean technically could've been written only to work for the present day snapshot galaxies, it would've been easier, but that's no fun c:
    # traces the biggest galaxy if a merger occurs
    keys = read.list_of_keys
    # set initial condition
    galaxy_list = []
    current_galaxy = galaxy
    first = None # first time the mass crosses the threshold
    # a list of keys that come after the given key in the list
    next_keys = keys[keys.index(key):]
    for current_key in next_keys:
        prev_galaxy = m_preimage(current_key, current_galaxy)
        if prev_galaxy is None:
            if first is not None:
                galaxy_list.append((current_key, current_galaxy))
                break
            else:
                break
        else:
            if first is None:
                if prev_galaxy[var] < threshold < current_galaxy[var]:
                    first = (current_key, current_galaxy)
                    last = (keys[keys.index(current_key) + 1], prev_galaxy)
                    galaxy_list.append((current_key, current_galaxy))
            else:
                galaxy_list.append((current_key, current_galaxy))
                if prev_galaxy[var] < threshold < current_galaxy[var]:
                    last = (keys[keys.index(current_key) + 1], prev_galaxy)
        current_key = keys[keys.index(current_key) + 1]
        current_galaxy = prev_galaxy
    if galaxy_list == []:
        return None
    else:
        region = galaxy_list[:(galaxy_list.index(last)+1)]
        return region

def preimage(key, galaxy):
    # get previous galaxies that are the pre image of the input galaxy
    keys = read.list_of_keys
    if key == keys[-1]:
        return []
    else:
        # index 0 returns current number, 1 returns next number
        galaxies = [prev_galaxy for prev_galaxy in read.galaxy_data[keys[keys.index(key)+1]] if galaxy.current == prev_galaxy.next]
        return galaxies

# need to include tracing children, that's a thing right?
def history(key, galaxy):
    # traces the history of a galaxy. It will return a list of tuples where each tuple describes the galaxy at a different snapshot in reverse chronological order
    keys = read.list_of_keys
    # set initial condition
    galaxy_list = [(key, galaxy)]
    current_galaxy = galaxy
    # a list of keys that come after the given key in the list
    next_keys = keys[-(len(keys) - keys.index(key)):] # I'm not sure why this version doesn't work, thanks probie? keys[keys.index(key) + 1:]
    for current_key in next_keys:
        galaxies = preimage(current_key, current_galaxy)
        if len(galaxies) == 0:
            break
        elif len(galaxies) == 1:
            galaxy_list.append((current_key, galaxies[0]))
        else:
            galaxies = [g for g in galaxies if g.current == current_galaxy.previous]
            galaxy_list.append((current_key, galaxies[0]))
        current_key = keys[keys.index(current_key) + 1]
        current_galaxy = galaxies[0]
    return galaxy_list

def evolution(key, galaxy, threshold, var):
    # takes the midpoint of the section of the list that crosses the threshold
    galaxies = history(key, galaxy)
    cross = [n for n,(cg,pg) in enumerate(zip(galaxies,galaxies[1:])) if cg[1][var] > threshold > pg[1][var]]
    if cross == []:
        return None
    else:
        first, last = cross[0], cross[-1]
        # since mass can go down below the threshold, if this occurs in present day, we include it in the region (it'll eventually go back up)
        if galaxy[var] < threshold:
            region = galaxies[:(last+2)]
        else:
            region = galaxies[first:last+2]
        mid = len(region) / 2
        if mid.is_integer():
            return region[int(mid)]
        else:
            lower = region[int(mid) - 1]
            upper = region[int(mid)]
            if region[-1][0].redshift - lower[0].redshift < upper[0].redshift - region[0][0].redshift:
                return lower
            else:
                return upper
