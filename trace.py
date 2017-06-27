import read
import init

# traces the galaxy mergers and returns the redshift when something is first above a certain mass

data = None

def retrieve():
    global data
    keys = read.list_of_keys
    objects = []
    M_stellar = init.M_stellar
    M_dm = init.M_dm
    M_bh = init.M_bh
    item = init.item
    if M_stellar is not None:
        var = 6
        obj = M_stellar
        err = 'stars'
    elif M_dm is not None:
        var = 7
        obj = M_dm
        err = 'dark matter haloes'
    elif M_bh is not None:
        var = 8
        obj = M_bh
        err = 'black holes'
    else:
        var = None

# if only short code always ran faster
# blame phil's file for this?

    for i in range(0, len(keys) - 1):
        for galaxy in read.galaxy_data[keys[i]]:
            for prev_galaxy in read.galaxy_data[keys[i+1]]:
                # 1. check that the previous galaxy is below the threshold mass - if it isn't, it already isn't what we're looking for
                # 2. find the pre-image of the galaxy that you want
                # 3. check that it has just passed the threshold mass
                # 1 and 3 can be done together, but this makes the code run slightly faster.
                if prev_galaxy[var] < obj and galaxy[2] == prev_galaxy[0] and galaxy[var] > obj:
                    if item == 'redshift':
                        objects.append(key[i][0])
                    if item == 'stellar':
                        objects.append(galaxy[6])
                    if item == 'dark matter':
                        objects.append(galaxy[7])
                    if item == 'black hole':
                        objects.append(galaxy[8])

    if objects != []:
        data = objects
    else:
        raise ValueError('no ' + err + ' found at the given mass')
