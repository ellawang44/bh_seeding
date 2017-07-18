import read
import distance
#for now
import pylab

# testing file

s5 = []
m = []

for galaxy in read.galaxy_data[(0, 1000)]:
    s5dist = distance.s5((0, 1000), galaxy)
    s5.append(s5dist)

#for now, this should be in main
pylab.hist(s5, bins = 100)
pylab.xlabel('s5 distance')
pylab.ylabel('number')
pylab.show()

'''

for galaxy in read.galaxy_data[(0, 1000)]:
    s5dist = distance.s5((0, 1000), galaxy)
    sm = galaxy.stellar_mass
    s5.append(s5dist)
    m.append(sm)

pylab.scatter(m, s5)
pylab.xlabel('stellar mass')
pylab.ylabel('s5 distance')
pylab.show()
'''
