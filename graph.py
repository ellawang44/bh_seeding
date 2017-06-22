import read
from init import *
import pylab
import snapshot

#this file is entirely broken
#jk I fixed it, but I don't want this file lol and it will be gone soon

data = snapshot.data

'''
#gets the coords
xcoord = [i[0] for i in data]
ycoord = [i[1] for i in data]
zcoord = [i[2] for i in data]
'''

dm = [i[4] for i in data]
bh = [i[5] for i in data if i[5] != float("-inf")]

pylab.hist(bh, bins = 100)
pylab.show()

pylab.hist(dm, bins = 100)
pylab.show()

#have a look at pdb library
