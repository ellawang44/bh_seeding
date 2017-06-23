import read
from init import redshift

#returns the data for the redshift closest to the one givenr

if redshift == None:
    data = None
else:
    keys = read.halo_data.keys()
    lower, upper = (0, None), (100, None)
    for i in keys:
        if i[0] < redshift and i[0] > lower[0]:
            lower = i
        elif i[0] > redshift and i[0] < upper[0]:
            upper = i
        else:
            pass
        if lower[0] - redshift < upper[0] - redshift:
            key = lower
        else:
            key = upper
        data = read.halo_data[key]
