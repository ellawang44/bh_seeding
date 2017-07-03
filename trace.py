import read
import init

# considers the galaxy mergers that occur and returns either redshift, stellar mass, black hole mass or dark matter halo mass when the given object first crosses the given mass
# except treats dark matter halo slightly differently. The dark matter halo is not monotomically increasing due to the friends of friends halo finder. We take the range over which it crosses the threshold mass and pick the snapshot in the middle

data = None

def retrieve():
    global data
    keys = read.list_of_keys
    objects = []
    if init.M_stellar is not None:
        var = 6
        obj = init.M_stellar
        err = 'stars'
    elif init.M_dm is not None:
        var = 7
        obj = init.M_dm
        err = 'dark matter haloes'
    elif init.M_bh is not None:
        var = 8
        obj = init.M_bh
        err = 'black holes'
    else:
        var = None

    # print file containing snapshots and galaxy numbers
    if init.print_file == True:
        f = open(str(err) + ' of mass ' + str(int(obj)) + '.txt', 'w')
        f.write('snapshot \t galaxy number \n')

    # silly friends of friends halo finder
    # not generalised to pull out everything yet, only pulls out black hole information, sorry
    if var == 7:
        for pres_galaxy in read.galaxy_data[keys[0]]:
            # initiate all the variables needed to trace a particular galaxy
            f = None
            current_key = keys[1]
            # get the previous set of galaxies, 1 snapshot earlier than the current
            galaxies = [prev_galaxy for prev_galaxy in read.galaxy_data[current_key] if prev_galaxy[1] == pres_galaxy[0]]
            # newly created galaxy at present day
            if len(galaxies) == 0:
                if galaxies[0][7] > obj:
                    objects.append(galaxies[8])
            elif len(galaxies) == 1:
                for galaxy in galaxies:
                    # update the current key
                    current_key = keys[keys.index(current_key) + 1]
                    for prev_galaxy in read.galaxy_data[current_key]:
                        # find the right galaxy to trace
                        if galaxy[0] == prev_galaxy[1]:
                            if f is None and galaxy[7] > obj and obj > prev_galaxy[7]:
                                    # need to set new things
                                    # regret updating current_key?
                                    f = keys[keys.index(current_key) - 1]
                                    a = list(f)
                                    a.append(list(galaxy))
                                    b = list(current_key)
                                    b.append(list(prev_galaxy))
                                    # initiate list, list contains tuples with current_key and galaxy number
                                    l_keys = [tuple(a), tuple(b)]
                            if f is not None:
                                c = list(current_key)
                                c.append(list(prev_galaxy))
                                l_keys.append(tuple(c))
                                if galaxy[7] > obj > prev_galaxy[7]:
                                    # update last key
                                    l = tuple(c)
                    # take the list till last, might have off by 1 error, check
                    galaxy_range = l_keys[:l_keys.index(l)]
                    # we'll floor it for now, can change it in the future, but Phil said it didn't matter, we'll see how un-lazy I am then, is that even a word?
                    # needs better name, might have off by 1 error, check
                    app = galaxy_range[len(galaxy_range) // 2]
                    print(app[2][8]) # this is for debugging only, remove later
                    objects.append(app[2][8])
                    if init.print_file == True:
                        f.write(str(app[1]) + '\t' + str(app[2][0]))
            else:
                # uhh if we have more than 1 galaxy what do? :(

    for i in range(0, len(keys) - 1):
        for galaxy in read.galaxy_data[keys[i]]:
            # decide what item to obtain histogram data for
            if init.item == 'stellar':
                item = galaxy[6]
            elif init.item == 'black hole':
                item = galaxy[8]
            else:
                item = keys[i][0]
            for prev_galaxy in read.galaxy_data[keys[i+1]]:
                # 1. check that the previous galaxy is below the threshold mass - if it isn't, it already isn't what we're looking for
                # 2. find the pre-image of the galaxy that you want
                # 3. check that it has just passed the threshold mass
                # 1 and 3 can be done together, but this makes the code run slightly faster (I think)
                # plz fix, it currently adds 2 blackholes if a merger pushes it over the threshold
                if prev_galaxy[var] < obj and galaxy[2] == prev_galaxy[0] and galaxy[var] > obj:
                    objects.append(item)
                    if init.print_file == True:
                        f.write(str(int(keys[i][1])) + ' \t ' + str(int(galaxy[0])) + ' \n')

    # gotta close the file so Probie's computer (and Windows) doesn't get annoyed
    if init.print_file == 'True':
        f.close()

    if objects != []:
        data = objects
    else:
        raise ValueError('no ' + err + ' found at the given mass')
