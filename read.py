from collections import defaultdict, namedtuple

# reads in the data
f = open('data/halo_data.dat','r')
next(f)

# name tuple so we can refer to each bit of data by name instead of indexing
galaxy_data = namedtuple('galaxy_data', ['xcoord', 'ycoord', 'zcoord', 'stellar_mass', 'dark_matter_mass', 'black_hole_mass'])

# stores the current key so we can update the entry in the for-loop
current_key = ('redshift', 'snapshot number')

#if the key does not exist, create key and set value to []
halo_data = defaultdict(lambda: [])

# builds dictionary
for line in f:
    line = line.split()
    data = tuple([float(i) for i in line])
    if len(data) == 2:
        # create new key
        current_key = data
    elif len(data) == 6:
        # append new data to existing value in key
        halo_data[current_key].append(galaxy_data._make(data))
    else:
        raise ValueError('unexpected line in input file under (redshift, snapshot):' + str(current_key))
