import read

# if the dark matter halo dips below the threshold before present day, but was above previously, the last couple of frames when it was below is not included currently in the region. Include this is you get time (doesn't make that much of a difference)

def preimage(key, galaxy):
    # get previous galaxies that are the pre image of the input galaxy
    keys = read.list_of_keys
    if key == keys[-1]:
        return []
    else:
        galaxies = [prev_galaxy for prev_galaxy in read.galaxy_data[keys[keys.index(key)+1]] if galaxy[0] == prev_galaxy[1]]
        return galaxies

def m_preimage(key, galaxy):
    # get the biggest galaxy in te preimage of the input galaxy
    keys = read.list_of_keys
    if key == keys[-1]:
        return None
    else:
        prev_galaxy = [prev_galaxy for prev_galaxy in read.galaxy_data[keys[keys.index(key)+1]] if galaxy[2] == prev_galaxy[0]]
        if prev_galaxy == []:
            return None
        else:
            return prev_galaxy[0]

def region(key, galaxy, threshold, var):
    # traces the evolution of 1 galaxy only. It will return a list of tuples where each tuple describes the galaxy at a different snapshot in reverse chronological order
    # I mean technically could've been written only to work for the present day snapshot galaxies, it would've been easier, but that's no fun c:
    # traces the biggest galaxy if a merger occurs
    keys = read.list_of_keys
    # set initial condition
    galaxy_list = []
    current_galaxy = galaxy
    first = None # f is the first time the mass crosses the threshold
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

def midpoint(key, galaxy, threshold, var):
    # takes the mid point of the section of the list that crosses the threshold
    galaxy_range = region(key, galaxy, threshold, var)
    if galaxy_range is None:
        return None
    else:
        mid = len(galaxy_range) / 2
        if not mid.is_integer():
             return galaxy_range[int(mid)]
        else:
            # return the snapshot with the redshift closest to the center
            lower = galaxy_range[int(mid)-1]
            upper = galaxy_range[int(mid)]
            if (galaxy_range[-1][0][0] - lower[0][0]) < (upper[0][0] - galaxy_range[0][0][0]):
                return lower
            else:
                return upper
