from collections import defaultdict, namedtuple

# name tuple so we can refer to each bit of data by name instead of indexing
key_naming = namedtuple('key_data', ['redshift', 'snapshot'])
galaxy_naming_short = namedtuple('galaxy_data', ['current', 'next', 'previous', 'present_day', 'xcoord', 'ycoord', 'zcoord', 'stellar_mass', 'dark_matter_mass', 'black_hole_mass', 'gas_mass'])
galaxy_naming_long = namedtuple('galaxy_data', ['current', 'next', 'previous', 'present_day', 'xcoord', 'ycoord', 'zcoord', 'stellar_mass', 'dark_matter_mass', 'black_hole_mass', 'gas_mass', 'acc_rate', 'density'])

class GalaxyData:
    def __init__(self, read_data):
        if type(read_data) == str:
            self.read_data = FileData(read_data)
        else:
            self.read_data = read_data

class FileData:
    def __init__(self,name):
        # reads in the data
        halo = open('data/halo_data' + name + '.dat','r')
        tree = open('data/tree_data' + name + '.dat','r')
        # skip the first line of the file, the name of the columns
        next(halo)
        next(tree)

        # stores the current key so we can update the entry in the for-loop
        current_key = ('redshift', 'snapshot number')
        list_of_keys = []

        # if the key does not exist, create key and set value to []
        galaxy_data = defaultdict(lambda: [])
        key_data = defaultdict(lambda: [])

        # builds dictionary
        for line_h, line_t in zip(halo, tree):
            line_h = line_h.split()
            line_t = line_t.split()
            data_h = tuple([float(i) for i in line_h])
            data_t = tuple([float(i) for i in line_t])
            if len(data_h) == 2 and data_h == data_t:
                # create new key,
                current_key = data_h
                list_of_keys.append(key_naming._make(current_key))
            elif len(data_h) == 9 and len(data_t) == 4:
                # append new data to existing value in key
                galaxy_data[current_key].append(galaxy_naming_long._make(data_t + data_h))
            elif len(data_h) == 7 and len(data_t) == 4:
                # append new data to existing value in key
                galaxy_data[current_key].append(galaxy_naming_short._make(data_t + data_h))
            else:
                print(data_h, data_t)
                raise ValueError('unexpected line in input files under (redshift, snapshot):' + str(current_key))
        self.galaxy_data = galaxy_data
        self.key_data = key_data
        self.list_of_keys = list_of_keys
