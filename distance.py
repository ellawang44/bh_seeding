from read import GalaxyData
import numpy

class Distance (GalaxyData):
    def s5(self, key, galaxy):
        #print(self.read_data.galaxy_data[key])
        galaxies = [(self.distance(gal, galaxy), gal) for gal in self.read_data.galaxy_data[key] if gal != galaxy]
        galaxies.sort()
        min5 = galaxies[:5]
        if len(min5) == 5:
            return min5[-1][0]

    def distance(self, gal, galaxy):
        sim_box_size = 25000/0.7 # simulation box size
        x = abs(gal.xcoord - galaxy.xcoord)
        y = abs(gal.ycoord - galaxy.ycoord)
        z = abs(gal.zcoord - galaxy.zcoord)
        dist = numpy.sqrt(min(x, sim_box_size - x)**2 + min(y, sim_box_size - y)**2 + min(z, sim_box_size - z)**2)
        return dist
