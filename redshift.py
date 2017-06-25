import read
import numpy
import init

#returns the data for the redshift closest to the one given

data = None

def retrieve():
    global data
    redshift = init.redshift
    if redshift is not None:
        keys = read.halo_data.keys()
        # set initial redshifts
        lower, upper = (0, None), (numpy.inf, None)
        # gets the two redshifts closest to the input redshift
        for i in keys:
            if lower[0] < i[0] < redshift:
                lower = i
            elif redshift < i[0] < upper[0]:
                upper = i
            # compares the two redshifts and returns the closest
            if lower[0] - redshift < upper[0] - redshift:
                key = lower
            else:
                key = upper
    data = read.halo_data[key]
