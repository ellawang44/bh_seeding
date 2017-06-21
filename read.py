#reads in the data
f = open('data/halo_data.dat','r')
next(f)

#creates dictionary
halo_data = {}
#stores the current key so we can update the entry in the for-loop
current_key = ("redshift", "snapshot number")
list_of_keys = []

for line in f:
    line = line.split()
    data = [float(i) for i in line]
    if len(line) == 2:
        current_key = (data[0], data[1])
        list_of_keys.append(current_key)
        halo_data.setdefault(current_key, [])
    elif len(line) == 6:
        val = halo_data.get(current_key)
        val.append(tuple(data))
        halo_data[current_key] = val
    else:
        print("error: unexpected line in input file under (redshift, snapshot):" ++ str(current_key))


#print(list_of_keys)
#print(halo_data)
