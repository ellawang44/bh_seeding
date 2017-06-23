import read
from init import snapshot

#returns the data in the given snapshot

key = "initial key"

if snapshot == None:
    data = None
else:
    for i in read.halo_data.keys():
        if i[1] == snapshot:
            key = i
        else:
            pass

if key == "initial key":
    print("error: snapshot does not exist")
    quit()
else:
    data = read.halo_data[key]
