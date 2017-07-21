import init
from read import GalaxyData

class Snapshot (GalaxyData):
    # matches snapshot to key in dictionary
    def __init__(self, read_data):
        super(Snapshot, self).__init__(read_data)
        snapshot = init.snapshot
        if snapshot is not None:
            for i in self.read_data.list_of_keys:
                if i.snapshot == snapshot:
                    self.key = i
        # if key corresponding to the given snapshot isn't found
        if key == 'initial key':
            raise ValueError('snapshot does not exist')
