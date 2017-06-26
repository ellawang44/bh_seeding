import read
import init

key = 'initial key'
data = None

# matches snapshot to key in dictionary

def retrieve():
    global data
    snapshot = init.snapshot
    if snapshot is not None:
        for i in read.list_of_keys:
            if i[1] == snapshot:
                key = i

    #retrieves data stored in the key

    if key == 'initial key':
        raise ValueError('snapshot does not exist')
    else:
        data = read.galaxy_data[key]
