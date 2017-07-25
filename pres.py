import init
import history
from read import GalaxyData

class Pres (GalaxyData):
    def __init__(self, read_data):
        super(Pres, self).__init__(read_data)
        hist = history.History(self.read_data)
        pres_key = (0, 1000)
        gals = []
        if init.M_stellar is not None:
            var = 7 # stellar mass
            obj = init.M_stellar
        elif init.M_dm is not None:
            var = 8 # dark matter mass
            obj = init.M_dm
        elif init.M_bh is not None:
            var = 9 # black hole mass
            obj = init.M_bh
        else:
            var = None
        for galaxy in self.read_data.galaxy_data[pres_key]:
            gal = hist.present(pres_key, galaxy, obj, var)
            if gal is not None:
                gals.append(gal)

        if gals != []:
            self.data = gals
        else:
            raise ValueError('Galaxies need to cross over the threshold.')
