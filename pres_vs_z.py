import snapshot
import init
from read import GalaxyData

class PresVsZ (GalaxyData):
    def __init__(self, read_data):
        super(PresVsZ, self).__init__(read_data)
        f = open('black holes of mass 5.txt', 'r')
        next(f)

        z = []
        m = []
        pres_key = (0, 1000)

        for line in f:
            line = line.split()
            dat = [int(i) for i in line]
            init.snapshot = dat[0] # set snapshot number
            key = snapshot.key
            redshift = key.redshift
            old_galaxy = self.read_data.galaxy_data[key][dat[1]]
            pres_galaxy_no = int(old_galaxy.present_day)
            galaxy = self.read_data.galaxy_data[pres_key][pres_galaxy_no]
            m.append(galaxy.stellar_mass)
            z.append(redshift)

        #for now, even though this should be in main
        '''
        pylab.scatter(m, z)
        pylab.title('bh = 5')
        pylab.xlabel('present day stellar mass')
        pylab.ylabel('redshift')
        pylab.show()
        '''
