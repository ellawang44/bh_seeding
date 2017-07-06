import read
import init
import midpoint

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
    if init.print_file:
        f = open(str(err) + ' of mass ' + str(int(obj)) + '.txt', 'w')
        f.write('snapshot \t galaxy number \n')

    # if black hole mass, then it is monotonically increasing, and we can do what we did before.
    if var == 8:
        for key in keys:
            for galaxy in read.galaxy_data[key]:
                prev_galaxy = midpoint.m_preimage(key, galaxy)
                if prev_galaxy is not None:
                    if prev_galaxy[var] < obj < galaxy[var]:
                        if init.item == 'stellar':
                            objects.append(galaxy[6])
                        elif init.item == 'dark matter':
                            objects.append(galaxy[7])
                        elif init.item == 'black hole':
                            objects.append(galaxy[8])
                        else:
                            objects.append(key[0])
                        if init.print_file:
                            f.write(str(int(keys[i][1])) + ' \t ' + str(int(galaxy[0])) + ' \n')
        '''
        for i in range(0, len(keys) - 1):
            for galaxy in read.galaxy_data[keys[i]]:
                # decide what item to obtain histogram data for
                if init.item == 'stellar':
                    item = galaxy[6]
                elif init.item == 'dark matter':
                    item = galaxy[7]
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
                        if init.print_file:
                            f.write(str(int(keys[i][1])) + ' \t ' + str(int(galaxy[0])) + ' \n')
                            '''
    else:
        for galaxy in read.galaxy_data[keys[0]]:
            frame = (midpoint.midpoint(keys[0], galaxy, obj, var))
            if frame is not None:
                if init.item == 'stellar':
                    objects.append(frame[1][6])
                elif init.item == 'dark matter':
                    objects.append(frame[1][7])
                elif init.item == 'black hole':
                    objects.append(frame[1][8])
                else:
                    objects.append(frame[0][0])
                if init.print_file:
                    f.write(str(int(frame[0][1])) + '\t' + str(int(frame[1][0])) + '\n')

    # gotta close the file so Probie's computer (and Windows) doesn't get annoyed
    if init.print_file:
        f.close()

    if objects != []:
        data = objects
    else:
        raise ValueError('no ' + err + ' found at the given mass')
