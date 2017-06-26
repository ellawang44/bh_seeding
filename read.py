from collections import defaultdict, namedtuple

# reads in the data
halo = open('data/halo_data.dat','r')
next(halo)
tree = open('data/tree_data.dat','r')
next(tree)

# name tuple so we can refer to each bit of data by name instead of indexing
naming_data = namedtuple('galaxy_data', ['xcoord', 'ycoord', 'zcoord', 'stellar_mass', 'dark_matter_mass', 'black_hole_mass', 'current', 'next', 'previous'])

# stores the current key so we can update the entry in the for-loop
current_key = ('redshift', 'snapshot number')
list_of_keys = []

#if the key does not exist, create key and set value to []
galaxy_data = defaultdict(lambda: [])

# builds dictionary
for line_h, line_t in zip(halo, tree):
    line_h = line_h.split()
    line_t = line_t.split()
    data_h = tuple([float(i) for i in line_h])
    data_t = tuple([float(i) for i in line_t][:3])
    if len(data_h) == 2 and data_h == data_t:
        # create new key,
        current_key = data_h
        list_of_keys.append(current_key)
    elif len(data_h) == 6 and len(data_t) == 3:
        # append new data to existing value in key
        galaxy_data[current_key].append(naming_data._make(data_t + data_h))
    else:
        raise ValueError('unexpected line in input files under (redshift, snapshot):' + str(current_key))
