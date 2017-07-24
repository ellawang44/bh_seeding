import read
import trace
import redshift
import snapshot
import pylab
import init
from optparse import OptionParser, OptionGroup

parser = OptionParser()

# reading in different files
parser.add_option('-f', '--file', type = 'string', dest = 'file', help = 'Determines the input file. Can also parse galaxy data.')

# data for a specific redshift/snapshot
parser.add_option('-z', '--redshift', type = 'float', dest = 'redshift', help = 'takes the data for the redshift closest to the given redshift. Needs to be used in conjuncture with "--data". The bin size of the histogram can be changed with "--bin", the default is 100.')

parser.add_option('-s', '--snapshot', type = 'int', dest = 'snapshot', help = 'takes the data for the specific snapshot. Needs to be used in conjuncture with "--data". The bin size of the histogram can be changed with "--bin", the default is 100.')

parser.add_option('--data', type = 'string', dest = 'data', help = 'Determines what data to pick from the galaxy. The possible inputs are "xcoord", "ycoord", "zcoord", "stellar", "dark matter" and "black hole".')

#frame = OptionGroup(parser,"redshift + xcoord")
#frame.add_option('-z', '--redshift', type = 'float', dest = 'redshift', help = 'takes the data for the redshift closest to the given redshift. Needs to be used in conjuncture --xcoord, --ycoord, --zcoord, --stellar, --darkmatter or --blackhole. Include the desired tag with any float, this float will not be read in. Also needs to be given the number of bins to include in the histogram, e.g: --bin 100.')
#parser.add_option_group(frame)


# parser.add_option('-z', '--redshift', type = 'float', dest = 'redshift', help = 'takes the data for the redshift closest to the given redshift. Needs to be used in conjuncture --xcoord, --ycoord, --zcoord, --stellar, --darkmatter or --blackhole. Include the desired tag with any float, this float will not be read in. Also needs to be given the number of bins to include in the histogram, e.g: --bin 100.')
# data for the coordinates

# parser.add_option('--xcoord', type = 'float', dest = 'xcoord', help = 'takes the data for the x coordinate. Needs to be used in conjuncture --snapshot or --redshift.')
parser.add_option('--ycoord', type = 'float', dest = 'ycoord', help = 'takes the data for the y coordinate. Needs to be used in conjuncture --snapshot or --redshift.')
parser.add_option('--zcoord', type = 'float', dest = 'zcoord', help = 'takes the data for the z coordinate. Needs to be used in conjuncture --snapshot or --redshift.')
# range around mass
parser.add_option('-r', '--range', type = 'float', dest = 'range', help = 'range around the given mass. e.g: if r = 2 and m = 5, then the data will contain objects in conjuncture mass from 3 to 7. By default, r = 1. Needs to be used in conjuecture with --stellar, --darkmatter or --blackhole.')
# data for mass
parser.add_option('-m', '--stellar', type = 'float', dest = 'stellar', help = 'If used alone, will trace galaxy merges and return the redshift when a particular galaxys stellar mass first goes above the input mass. If used in conjuncture with --range: for the given stellar mass, takes all the haloes that has stellar mass in conjuncturein the given range around the specified mass and returns the redshift at which they occur and the number of times it occurs at that redshift. If used in conjuncture --snapshot or --redshift: returns the distribution of stellar masses for a the given snapshot/redshift.')
parser.add_option('-d', '--darkmatter', type = 'float', dest = 'darkmatter', help = 'If used alone, will trace galaxy merges and return the redshift when a particular galaxys dark matter mass first goes above the input mass. If used in conjuncture with --range: for the given dark matter mass, takes all the haloes that has dark matter mass in conjuncturein the given range around the specified mass and returns the redshift at which they occur and the number of times it occurs at that redshift. If used in conjuncture --snapshot or --redshift: returns the distribution of dark matter halo masses for a the given snapshot/redshift.')
parser.add_option('-b', '--blackhole', type = 'float', dest = 'blackhole', help = 'If used alone, will trace galaxy merges and return the redshift when a particular galaxys black hole mass first goes above the input mass. If used in conjuncture with --range: for the given black hole mass, takes all the haloes that has black hole mass in conjuncturein the given range around the specified mass and returns the redshift at which they occur and the number of times it occurs at that redshift. If used in conjuncture --snapshot or --redshift: returns the distribution of black hole masses for a the given snapshot/redshift.')
# pick the mass data to take for a the object at the given mass. E.g: return dark matter haloes for all black holes at mass 5.
parser.add_option('--object', type = 'string', dest = 'object', help = 'picks the mass data for the input object, can be "stellar", "black hole", "dark matter" or "redshift". Used in conjuncture with --stellar, --darkmatter or --blackhole. e.g: --darkmatter 10 --object blackhole returns the masses of black holes which have a darkmatter halo of just above 10 in a histogram. Can also be used with --txt to create a txt file which contains all the snapshot and galaxy numbers of the histogram.')

# number of bins in histogram
parser.add_option('--bin', type = 'int', dest = 'bin', help = 'Number of bins drawn on the histgram for data for a single snapshot or redshift.')

# print text file of snapshot number and galaxy number or not
parser.add_option('--txt', dest = 'txt', default = False, help = 'creates a .txt file which contains the snapshot and galaxy number. Used in conjuecture with object.')

if __name__ == '__main__':
    (options, args) = parser.parse_args()

    if options.file:
        init.file = options.file

    read_data = read.FileData(init.file_name)
    binnum = 100 # default number of bins
    # used for all histograms so it's up here
    if options.bin:
        binnum = options.bin

    if options.data == 'xcoord':
        var = 4
        name = 'x-coordinates'
    elif options.data == 'ycoord':
        var = 5
        name = 'y-coordinates'
    elif options.data == 'zcoord':
        var = 6
        name = 'z-coordinates'
    elif options.data == 'stellar':
        var = 7
        name = 'stellar mass'
    elif options.data == 'dark matter':
        var = 8
        name = 'dark matter mass'
    elif options.data == 'black hole':
        var = 9
        name = 'black hole mass'
    else:
        raise ValueError('not a valid data input')

    # graph for a single frame in the simulation
    galaxies = None
    if options.snapshot:
        init.snapshot = options.snapshot
        key = snapshot.Snapshot(init.file_name).key
        galaxies = read_data.galaxy_data[key]
    if options.redshift or options.redshift == 0:
        init.redshift = options.redshift
        key = redshift.Redshift(init.file_name).key
        galaxies = read_data.galaxy_data[key]
    if galaxies is not None:
        data = [g[var] for g in galaxies]
        # filter out -inf
        if var == 9:
            data = [i for i in data if i != float('-inf')]
        pylab.hist(data, bins = binnum)
        pylab.xlabel(name)
        pylab.ylabel('number')
        pylab.show()

    # graph for tracing the mass of an object in a galaxy
    if options.txt:
        init.print_file = True
    if options.object:
        init.item = options.object
        if options.stellar:
            init.M_stellar = options.stellar
            trace.retrieve()
            data = trace.data
            title = 'stellar mass = ' + str(options.stellar)
        if options.darkmatter:
            init.M_dm = options.darkmatter
            trace.retrieve()
            data = trace.data
            title = 'dark matter mass = ' + str(options.darkmatter)
        if options.blackhole:
            init.M_bh = options.blackhole
            trace.retrieve()
            data = trace.data
            title = 'black hole mass = ' + str(options.blackhole)
    data = None
    if data is not None:
        data = [i for i in data if i != float('-inf')]
        pylab.hist(data, bins = binnum)
        pylab.title(title)
        pylab.xlabel(options.object)
        pylab.ylabel('number')
        pylab.show()
