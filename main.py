import objects
import redshift
import snapshot
import pylab
import init
from optparse import OptionParser

parser = OptionParser()
# data for a specific redshift/snapshot
parser.add_option('-s', '--snapshot', type = 'int', dest = 'snapshot', help = 'takes the data for the specific snapshot. Needs to be used in conjuncture --xcoord, --ycoord, --zcoord, --stellar, --darkmatter or --blackhole. Include the desired tag with any float, this float will not be read in. Also needs to be given the number of bins to include in the histogram, e.g: --bin 100.')
parser.add_option('-z', '--redshift', type = 'float', dest = 'redshift', help = 'takes the data for the redshift closest to the given redshift. Needs to be used in conjuncture --xcoord, --ycoord, --zcoord, --stellar, --darkmatter or --blackhole. Include the desired tag with any float, this float will not be read in. Also needs to be given the number of bins to include in the histogram, e.g: --bin 100.')
# data for the coordinates
parser.add_option('--xcoord', type = 'float', dest = 'xcoord', help = 'takes the data for the x coordinate. Needs to be used in conjuncture --snapshot or --redshift.')
parser.add_option('--ycoord', type = 'float', dest = 'ycoord', help = 'takes the data for the y coordinate. Needs to be used in conjuncture --snapshot or --redshift.')
parser.add_option('--zcoord', type = 'float', dest = 'zcoord', help = 'takes the data for the z coordinate. Needs to be used in conjuncture --snapshot or --redshift.')
# range around mass
parser.add_option('-r', '--range', type = 'float', dest = 'range', help = 'range around the given mass. e.g: if r = 2 and m = 5, then the data will contain objects in conjuncture mass from 3 to 7. By default, r = 1. Needs to be used in conjuecture with --stellar, --darkmatter or --blackhole.')
# data for mass
parser.add_option('-m', '--stellar', type = 'float', dest = 'stellar', help = 'Gives stellar mass data. If used in conjuncture --range: for the given stellar mass, takes all the haloes that has stellar mass in conjuncturein the given range around the specified mass and returns the redshift at which they occur and the number of times it occurs at that redshift. If used in conjuncture --snapshot or --redshift: returns the distribution of stellar masses for a the given snapshot/redshift.')
parser.add_option('-d', '--darkmatter', type = 'float', dest = 'darkmatter', help = 'If used in conjuncture --range: for the given dark matter mass, takes all the haloes that has dark matter mass in conjuncturein the given range around the specified mass and returns the redshift at which they occur and the number of times it occurs at that redshift. If used in conjuncture --snapshot or --redshift: returns the distribution of dark matter halo masses for a the given snapshot/redshift.')
parser.add_option('-b', '--blackhole', type = 'float', dest = 'blackhole', help = 'If used in conjuncture --range: for the given black hole mass, takes all the haloes that has black hole mass in conjuncturein the given range around the specified mass and returns the redshift at which they occur and the number of times it occurs at that redshift. If used in conjuncture --snapshot or --redshift: returns the distribution of black hole masses for a the given snapshot/redshift.')
# number of bins in histogram
parser.add_option('--bin', type = 'int', dest = 'bin', help = 'number of bins drawn on the histgram for data for a single snapshot or redshift.')

if __name__ == '__main__':
    (options, args) = parser.parse_args()
    item = 'snapshot or redshift'
    data = []
    if options.snapshot:
        init.snapshot = options.snapshot
        item = snapshot
        item.retrieve()
    if options.redshift or options.redshift == 0:
        init.redshift = options.redshift
        item = redshift
        item.retrieve()
    # if --snapshot or --redshift is called
    if item != 'snapshot or redshift':
        name = 'initial'
        if options.xcoord:
            data = [i[3] for i in item.data]
            name = 'x-coordinates'
        elif options.ycoord:
            data = [i[4] for i in item.data]
            name = 'y-coordinates'
        elif options.zcoord:
            data = [i[5] for i in item.data]
            name = 'z-coordinates'
        elif options.stellar:
            data = [i[6] for i in item.data]
            name = 'stellar masses'
        elif options.darkmatter:
            data = [i[7] for i in item.data]
            name = 'dark matter masses'
        elif options.blackhole:
            data = [i[8] for i in item.data if i[8] != float('-inf')]
            name = 'black hole masses'
        else:
            raise ValueError('please parse second input. (help snapshot if unsure)')
    if data != [] and options.bin:
        binnum = options.bin
        pylab.hist(data, bins = binnum)
        pylab.xlabel(name)
        pylab.ylabel('counts')
        pylab.show()
    if options.range:
        init.r = options.range
        if options.stellar:
            init.M_stellar = options.stellar
        elif options.darkmatter:
            init.M_dm = options.darkmatter
        elif options.blackhole:
            init.M_bh = options.blackhole
        else:
            raise ValueError('please parse second input. (help range if unsure)')
        objects.retrieve()
        pylab.plot((objects.data)[0], (objects.data)[1])
        pylab.xlabel('redshift')
        pylab.ylabel('counts')
        pylab.show()
