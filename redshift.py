import read
import numpy
import init

#returns the data for the redshift closest to the one given

data = None

def retrieve():
    global data
    redshift = init.redshift
    if redshift is not None:
        keys = read.list_of_keys
        # set initial redshifts
        lower, upper = None, None
        # gets the two redshifts closest to the input redshift
        for i in keys:
            if i[0] >= redshift:
                upper = i
                lower = keys[keys.index(i) - 1]
                break
        # compares the two redshifts and returns the closest
        if lower[0] - redshift < upper[0] - redshift:
            key = lower
        else:
            key = upper
    data = read.galaxy_data[key]
