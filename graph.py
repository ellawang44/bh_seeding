import read
import pylab

key = (0.0,1000)
data = read.halo_data[key]

xcoord = [i[0] for i in data]
ycoord = [i[1] for i in data]
zcoord = [i[2] for i in data]

#checking that the halos are within the simulation
print(max(xcoord), max(ycoord), max(zcoord))
#looks good so far

#black holes histogram doesn't work currently, we need to filter out the -infinities, but filter is returning true or false... 
dm = [i[4] for i in data]
bh = [i[5] != float("-inf") for i in data]
print(bh)
print(dm)

pylab.hist(bh, bins = 100)
pylab.show()

pylab.hist(dm, bins = 100)
pylab.show()

#pdb library
