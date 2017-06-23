import read
from init import snapshot

key = "initial key"

# matches snapshot to key in dictionary

if snapshot is None:
    data = None
else:
    for i in read.halo_data.keys():
        if i[1] == snapshot:
            key = i
        else:
            pass

#retrieves data stored in the key

if key == "initial key":
    raise ValueError("snapshot does not exist")
else:
    data = read.halo_data[key]
