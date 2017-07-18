import read
import snapshot
import init
import distance
#for now
import pylab

# turn this entire thing into a function?
# make file name generalisable :(
# if I could do this I would've done it already for read.py :(
# probably wrong
f = open('black holes of mass 5.txt', 'r')
next(f)

s5 = []
m = []
pres_key = (0, 1000)

for line in f:
    line = line.split()
    dat = [int(i) for i in line]
    init.snapshot = dat[0] # set snapshot number
    snapshot.retrieve() # retrieve key from snapshot number
    key = snapshot.key
    old_galaxy = read.galaxy_data[key][dat[1]]
    pres_galaxy_no = int(old_galaxy.present_day)
    galaxy = read.galaxy_data[pres_key][pres_galaxy_no]
    s5dist = distance.s5(pres_key, galaxy) # get s5 distance
    if s5dist is not None:
        m.append(galaxy.dark_stellar_mass)
        s5.append(s5dist)

#for now, this should be in main
pylab.scatter(m, s5)
pylab.xlabel('dark matter mass')
pylab.ylabel('s5 distance')
pylab.show()
