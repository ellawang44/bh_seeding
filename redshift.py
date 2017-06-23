import read
import numpy
from init import redshift

#returns the data for the redshift closest to the one given

if redshift is None:
    data = None
else:
    keys = read.halo_data.keys()
    # set initial redshifts
    lower, upper = (0, None), (numpy.inf, None)
    # gets the two redshifts closest to the input redshift
    for i in keys:
        if i[0] < redshift and i[0] > lower[0]:
            lower = i
        elif i[0] > redshift and i[0] < upper[0]:
            upper = i
        else:
            pass
        # compares the two redshifts and returns the closest
        if lower[0] - redshift < upper[0] - redshift:
            key = lower
        else:
            key = upper
        data = read.halo_data[key]
