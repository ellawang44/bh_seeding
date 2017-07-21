import snapshot
import init
#for now
import pylab
from read import GalaxyData

class PresVsZ (GalaxyData):
    # turn this entire thing into a function?
    # make file name generalisable :(
    # if I could do this I would've done it already for read.py :(
    # probably wrong
    f = open('black holes of mass 5.txt', 'r')
    next(f)

    z = []
    m = []
    pres_key = (0, 1000)

    for line in f:
        line = line.split()
        dat = [int(i) for i in line]
        init.snapshot = dat[0] # set snapshot number
        snapshot.retrieve() # retrieve key from snapshot number
        key = snapshot.key
        redshift = key.redshift
        old_galaxy = self.read.galaxy_data[key][dat[1]]
        pres_galaxy_no = int(old_galaxy.present_day)
        galaxy = self.read.galaxy_data[pres_key][pres_galaxy_no]
        m.append(galaxy.stellar_mass)
        z.append(redshift)

    #for now, even though this should be in main
    '''
    tup = list(zip(m, s5))
    tup.sort()
    m = [i[0] for i in tup]
    s5 = [i[1] for i in tup]
    '''
    pylab.scatter(m, z)
    pylab.title('bh = 5')
    pylab.xlabel('present day stellar mass')
    pylab.ylabel('redshift')
    pylab.show()
