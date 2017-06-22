from collections import defaultdict

# reads in the data
f = open("data/halo_data.dat","r")
next(f)

# creates empty dictionary
halo_data = {}
# stores the current key so we can update the entry in the for-loop
current_key = ("redshift", "snapshot number")

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
        halo_data[current_key].append(data)
    else:
        print("error: unexpected line in input file under (redshift, snapshot):" ++ str(current_key))
        quit()
