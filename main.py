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

parser.add_option('--data', type = 'string', dest = 'data', help = 'Determines what data to pick from the galaxy. The possible inputs are "redshift", "xcoord", "ycoord", "zcoord", "stellar", "dark matter" and "black hole".')

#frame = OptionGroup(parser,"redshift + xcoord")
#frame.add_option('-z', '--redshift', type = 'float', dest = 'redshift', help = 'takes the data for the redshift closest to the given redshift. Needs to be used in conjuncture --xcoord, --ycoord, --zcoord, --stellar, --darkmatter or --blackhole. Include the desired tag with any float, this float will not be read in. Also needs to be given the number of bins to include in the histogram, e.g: --bin 100.')
#parser.add_option_group(frame)

# parser.add_option('--xcoord', type = 'float', dest = 'xcoord', help = 'takes the data for the x coordinate. Needs to be used in conjuncture --snapshot or --redshift.')
# parser.add_option('--ycoord', type = 'float', dest = 'ycoord', help = 'takes the data for the y coordinate. Needs to be used in conjuncture --snapshot or --redshift.')
# parser.add_option('--zcoord', type = 'float', dest = 'zcoord', help = 'takes the data for the z coordinate. Needs to be used in conjuncture --snapshot or --redshift.')
# data for mass
parser.add_option('-m', '--stellar', type = 'float', dest = 'stellar', help = 'Trace galaxy merges and return the redshift when a particular galaxys stellar mass first goes above the input mass.')
parser.add_option('-d', '--darkmatter', type = 'float', dest = 'darkmatter', help = 'If used alone, will trace galaxy merges and return the redshift when a particular galaxys dark matter mass first goes above the input mass. If used in conjuncture with --range: for the given dark matter mass, takes all the haloes that has dark matter mass in conjuncturein the given range around the specified mass and returns the redshift at which they occur and the number of times it occurs at that redshift. If used in conjuncture --snapshot or --redshift: returns the distribution of dark matter halo masses for a the given snapshot/redshift.')
parser.add_option('-b', '--blackhole', type = 'float', dest = 'blackhole', help = 'If used alone, will trace galaxy merges and return the redshift when a particular galaxys black hole mass first goes above the input mass. If used in conjuncture with --range: for the given black hole mass, takes all the haloes that has black hole mass in conjuncturein the given range around the specified mass and returns the redshift at which they occur and the number of times it occurs at that redshift. If used in conjuncture --snapshot or --redshift: returns the distribution of black hole masses for a the given snapshot/redshift.')
# pick the mass data to take for a the object at the given mass. E.g: return dark matter haloes for all black holes at mass 5.
# print file containing galaxies of interest
parser.add_option('--txt', action = 'store_true', dest = 'txt', help = 'outputs a helpful file.')

# number of bins in histogram
parser.add_option('--bin', type = 'int', dest = 'bin', help = 'Number of bins drawn on the histgram for data for a single snapshot or redshift.')

if __name__ == '__main__':
    (options, args) = parser.parse_args()

    if options.file:
        init.file = options.file

    read_data = read.FileData(init.file_name)
    binnum = 100 # default number of bins
    # used for all histograms so it's up here
    if options.bin:
        binnum = options.bin

    var, name = { 'redshift' : (0, 'redshift'),
                 'xcoord' : (4, 'x-coordinates'),
                 'ycoord' : (5, 'y-coordinates'),
                 'zcoord' : (6, 'z-coordinates'),
                 'stellar' : (7, 'stellar mass'),
                 'dark matter' : (8, 'dark matter mass'),
                 'black hole' : (9, 'black hole mass'),
                 None : (None, None)
            }[options.data]

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
        galaxies = [g[var] for g in galaxies]
        # filter out -inf
        if var == 9:
            galaxies = [i for i in galaxies if i != float('-inf')]
        pylab.hist(galaxies, bins = binnum)
        pylab.xlabel(name)
        pylab.ylabel('number')
        pylab.show()

    # graph for tracing the mass of an object in a galaxy
    # prints file output
    if options.txt:
        init.print_file = True
    data = None
    if options.stellar:
        init.M_stellar = options.stellar
        galaxies = trace.Trace(init.file_name).data
        title = 'stellar mass = ' + str(options.stellar)
    elif options.darkmatter:
        init.M_dm = options.darkmatter
        galaxies = trace.Trace(init.file_name).data
        title = 'dark matter mass = ' + str(options.darkmatter)
    elif options.blackhole:
        init.M_bh = options.blackhole
        galaxies = trace.Trace(init.file_name).data
        title = 'black hole mass = ' + str(options.blackhole)
    if options.data == 'redshift':
        data = [g[0][var] for g in galaxies]
    else:
        data = [g[1][var] for g in galaxies]
        data = [i for i in data if i != float('-inf')]
    if data is not None:
        pylab.hist(data, bins = binnum)
        pylab.title(title)
        pylab.xlabel(name)
        pylab.ylabel('number')
        pylab.show()

    # graph for present day data for galaxies of interest
