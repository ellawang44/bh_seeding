import read
import init

# decides what data to retrieve depending on input

data = None
def retrieve():
    global data
    r = init.r
    M_stellar = init.M_stellar
    M_dm = init.M_dm
    M_bh = init.M_bh
    if M_stellar is not None:
        var = 3
        obj = M_stellar
        err = 'stars'
    elif M_dm is not None:
        var = 4
        obj = M_dm
        err = 'dark matter haloes'
    elif M_bh is not None:
        var = 5
        obj = M_bh
        err = 'black holes'
    else:
        var = None

        # takes the redshifts for the chosen object
        if var is None:
            data = None
        else:
            objects = []
            for key, value in read.halo_data.items():
                current_redshift = key[0]
                counts = 0
                # gets the number of objects that satisfy the given mass range
                for i in value:
                    if obj - r < i[var] < obj + r:
                        counts += 1
                # build a tuple of the redshift and number if there is more than 0 objects that satisfy the mass range
                if counts != 0:
                    objects.append((current_redshift, counts))
            # if there are objects that satisfy the given mass range
            # gets the data ready for plotting
            if objects != []:
                redshift = []
                num = []
                # sadly the redshifts aren't sorted because dictionaries aren't sorted
                for i in sorted(objects):
                    redshift.append(i[0])
                    num.append(i[1])
                data = (redshift, num)
            else:
                raise ValueError('no ' + err + ' found within mass range ' + str(obj - r) + ' to ' + str(obj + r))
