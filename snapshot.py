import read
import init

key = 'initial key'
data = None

# matches snapshot to key in dictionary

def retrieve():
    global key
    snapshot = init.snapshot
    if snapshot is not None:
        for i in read.list_of_keys:
            if i.snapshot == snapshot:
                key = i
    # if key corresponding to the given snapshot isn't found
    if key == 'initial key':
        raise ValueError('snapshot does not exist')
