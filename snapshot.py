import read
import snapshot

key = 'initial key'
data = None

# matches snapshot to key in dictionary

def retrieve():
    snapshot = init.snapshot
    if snapshot is None:
        data = None
    else:
        for i in read.halo_data.keys():
            if i[1] == snapshot:
                key = i

    #retrieves data stored in the key

    if key == 'initial key':
        raise ValueError('snapshot does not exist')
    else:
        data = read.halo_data[key]
