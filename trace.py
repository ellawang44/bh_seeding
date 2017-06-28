import read
import init

# traces the galaxy mergers and returns the redshift when something is first above a certain mass

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

    # orint file containing snapshots and galaxy numbers
    if init.print_file == True:
        f = open(init.item + ' for ' + str(err) + ' of mass ' + str(int(obj)) + '.txt', 'w')
        f.write('snapshot \t galaxy number \n')

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
                item = key[i][0]
            for prev_galaxy in read.galaxy_data[keys[i+1]]:
                # 1. check that the previous galaxy is below the threshold mass - if it isn't, it already isn't what we're looking for
                # 2. find the pre-image of the galaxy that you want
                # 3. check that it has just passed the threshold mass
                # 1 and 3 can be done together, but this makes the code run slightly faster (I think)
                if prev_galaxy[var] < obj and galaxy[2] == prev_galaxy[0] and galaxy[var] > obj:
                    objects.append(item)
                    if init.print_file == True:
                        f.write(str(int(keys[i][1])) + ' \t ' + str(int(galaxy[0])) + ' \n')
    if objects != []:
        data = objects
    else:
        raise ValueError('no ' + err + ' found at the given mass')
