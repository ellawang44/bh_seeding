import read
import pylab

#even though the key is encoded as (redshift, snapshot) we only want to give the snapshot number in calling the key
#we also want to be able to edit the snapshot number in the main file and not a graphing file - so eventually this will become a dummy variable
snapshot = 1000

for i in read.halo_data.keys():
    if i[1] == snapshot:
        key = i
    else:
        print("error: snapshot does not exist")
data = read.halo_data[key]

'''
#gets the coords
xcoord = [i[0] for i in data]
ycoord = [i[1] for i in data]
zcoord = [i[2] for i in data]
'''

#fixed black holes histgram, I'm stupid.
dm = [i[4] for i in data]
bh = [i[5] for i in data if i[5] != float("-inf")]

pylab.hist(bh, bins = 100)
pylab.show()

pylab.hist(dm, bins = 100)
pylab.show()

#have a look at pdb library
