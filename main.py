import read
import trace
import redshift
import snapshot
import pres
import pylab
import init
from optparse import OptionParser, OptionGroup

parser = OptionParser()

# reading in different files
parser.add_option('-f', '--file', type = 'string', dest = 'file', help = 'Determines the input file. Can also parse galaxy data.')

# data for a specific redshift/snapshot
parser.add_option('-z', '--redshift', type = 'float', dest = 'redshift', help = 'takes the data for the redshift closest to the given redshift. Needs to be used in conjuncture with "--data". The bin size of the histogram can be changed with "--bin", the default is 100.')

parser.add_option('-s', '--snapshot', type = 'int', dest = 'snapshot', help = 'takes the data for the specific snapshot. Needs to be used in conjuncture with "--data". The bin size of the histogram can be changed with "--bin", the default is 100.')

# takes out the required data type
parser.add_option('--data', type = 'string', dest = 'data', help = 'Determines what data to pick from the galaxy. The possible inputs are "redshift", "xcoord", "ycoord", "zcoord", "stellar", "dark matter" and "black hole".')

# sets the threshold mass
parser.add_option('-m', '--stellar', type = 'float', dest = 'stellar', help = 'Trace galaxy merges and return the redshift when a particular galaxys stellar mass first goes above the input mass.')

parser.add_option('-d', '--darkmatter', type = 'float', dest = 'darkmatter', help = 'If used alone, will trace galaxy merges and return the redshift when a particular galaxys dark matter mass first goes above the input mass. If used in conjuncture with --range: for the given dark matter mass, takes all the haloes that has dark matter mass in conjuncturein the given range around the specified mass and returns the redshift at which they occur and the number of times it occurs at that redshift. If used in conjuncture --snapshot or --redshift: returns the distribution of dark matter halo masses for a the given snapshot/redshift.')

parser.add_option('-b', '--blackhole', type = 'float', dest = 'blackhole', help = 'If used alone, will trace galaxy merges and return the redshift when a particular galaxys black hole mass first goes above the input mass. If used in conjuncture with --range: for the given black hole mass, takes all the haloes that has black hole mass in conjuncturein the given range around the specified mass and returns the redshift at which they occur and the number of times it occurs at that redshift. If used in conjuncture --snapshot or --redshift: returns the distribution of black hole masses for a the given snapshot/redshift.')

# takes the present day image of the galaxies of interest
parser.add_option('--downsizing', action = 'store_true', dest = 'downsizing', help = 'Takes the selected data and outputs a scatter plot of the redshift along the x-axis and the data on the y-axis.')

# print file containing galaxies of interest
parser.add_option('--txt', action = 'store_true', dest = 'txt', help = 'outputs a file containing the galaxy number of galaxies that cross over the threshold and the snapshot number when they cross over.')

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

    # prints file output
    if options.txt:
        init.print_file = True

    # graph for tracing the mass of an object in a galaxy
    galaxies2 = None
    if options.stellar:
        init.M_stellar = options.stellar
        title = 'stellar mass = ' + str(options.stellar)
        galaxies2 = trace.Trace(init.file_name).data
    elif options.darkmatter:
        init.M_dm = options.darkmatter
        title = 'dark matter mass = ' + str(options.darkmatter)
        galaxies2 = trace.Trace(init.file_name).data
    elif options.blackhole:
        init.M_bh = options.blackhole
        title = 'black hole mass = ' + str(options.blackhole)
        galaxies2 = trace.Trace(init.file_name).data

    if galaxies2 is not None:
        if options.data == 'redshift':
            res = [g[0][var] for g in galaxies2]
        else:
            res = [g[1][var] for g in galaxies2]
        if options.downsizing:
            redshift = [g[0].redshift for g in galaxies2]
            # if black holes, need to filter out -inf
            if var == 9:
                filt = [g for g in zip(redshift, res) if g[1] != float('-inf')]
                redshift = [g[0] for g in filt]
                res = [g[1] for g in filt]
            pylab.scatter(redshift, res)
            pylab.title(title)
            pylab.xlabel('redshift')
            pylab.ylabel(name)
            pylab.show()
        else:
            if var == 9:
                res = [g for g in res if g != float('-inf')]
            pylab.hist(res, bins = binnum)
            pylab.title(title)
            pylab.xlabel(name)
            pylab.ylabel('number')
            pylab.show()
