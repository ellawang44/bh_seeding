import read
import trace
import redshift
import snapshot
import pylab
import init
import numpy
from collections import defaultdict
import matplotlib.pyplot as plt
from scipy import stats
from optparse import OptionParser
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

parser = OptionParser()

# ks test keromerogh's speamouth test?
# label the distribution numbers
# add error bars to the plot (possion error, sqrt(n))
# legend to the stats
# table for stats
# Gaussian expansion including skewness and kurtosis
# 3 SF for accuracy


# reading in different files
parser.add_option('-f', '--file', type = 'string', dest = 'file', help = 'Determines the input file. Can also parse galaxy data.')

# data for a specific redshift/snapshot
parser.add_option('-z', '--redshift', type = 'float', dest = 'redshift', help = 'Takes the data for the redshift closest to the given redshift. Needs to be used in conjuncture with "--data". The bin size of the histogram can be changed with "--bin", the default is 100.')

parser.add_option('-s', '--snapshot', type = 'int', dest = 'snapshot', help = 'Takes the data for the specific snapshot. Needs to be used in conjuncture with "--data". The bin size of the histogram can be changed with "--bin", the default is 100.')

# takes out the required data type
parser.add_option('--data', type = 'string', dest = 'data', help = 'Determines what data to pick from the galaxy. The possible inputs are "redshift", "xcoord", "ycoord", "zcoord", "stellar", "dark matter" and "black hole".')

# sets the threshold mass
parser.add_option('-m', '--stellar', type = 'float', dest = 'stellar', help = 'Sets the threshold stellar mass, galaxies that just pass above that threshold mass will be recorded. Use "--data" to determine what aspect of those galaxies to histogram. Use "--downsizing" to plot the redshift at which the galaxies first cross over the threshold vs the aspect of the galaxy selected by the data tag. Use "--txt" to output a txt file containing the galaxy number of the galaxies that just pass above the threshold mass and the snapshot at which it occurs.')

parser.add_option('-d', '--darkmatter', type = 'float', dest = 'darkmatter', help = 'Sets the threshold dark matter halo mass, galaxies that just pass above that threshold mass will be recorded. Use "--data" to determine what aspect of those galaxies to histogram. Use "--downsizing" to plot the redshift at which the galaxies first cross over the threshold vs the aspect of the galaxy selected by the data tag. Use "--txt" to output a txt file containing the galaxy number of the galaxies that just pass above the threshold mass and the snapshot at which it occurs.')

parser.add_option('-b', '--blackhole', type = 'float', dest = 'blackhole', help = 'Sets the threshold black hole mass, galaxies that just pass above that threshold mass will be recorded. Use "--data" to determine what aspect of those galaxies to histogram. Use "--downsizing" to plot the redshift at which the galaxies first cross over the threshold vs the aspect of the galaxy selected by the data tag. Use "--txt" to output a txt file containing the galaxy number of the galaxies that just pass above the threshold mass and the snapshot at which it occurs.')

# takes the present day image of the galaxies of interest
parser.add_option('--downsizing', action = 'store_true', dest = 'downsizing', help = 'Takes the selected data and outputs a scatter plot of the redshift along the x-axis and the data on the y-axis. Used together with "--data" and either "--stellar", "--darkmatter" or "--blackhole".')

# print file containing galaxies of interest
parser.add_option('--txt', action = 'store_true', dest = 'txt', help = 'outputs a file containing the galaxy number of galaxies that cross over the threshold and the snapshot number when they cross over. Used together with "--data" and either "--stellar", "--darkmatter" or "--blackhole".')

# print statistics of histogram
parser.add_option('--stats', action = 'store_true', dest = 'stats', help = 'prints to screen the statistics of the histogram.')

# number of bins in histogram
parser.add_option('--bin', type = 'int', dest = 'bin', help = 'Determines the number of bins drawn on the histgram.')

if __name__ == '__main__':
    (options, args) = parser.parse_args()

    # sets the correct file to read in
    if options.file:
        init.file_name = options.file

    read_data = read.FileData(init.file_name)
    binnum = 100 # default number of bins
    # changes the bin sizes used in histograms
    if options.bin:
        binnum = options.bin


    # sets the variable and name associated with the wanted data
    var, name = { 'redshift' : (0, 'redshift'),
                 'xcoord' : (4, 'x-coordinates'),
                 'ycoord' : (5, 'y-coordinates'),
                 'zcoord' : (6, 'z-coordinates'),
                 'stellar' : (7, r'log $M_{*}$ [\rm{M}_{\odot}]'),
                 'dark matter' : (8, r'log $M_{\rm DM}$ [\rm{M}_{\odot}]'),
                 'black hole' : (9, r'log $M_{\rm BH}$ [\rm M_{\odot}]'),
                 'gas' : (10, r'log $M_{\rm g}$ [\rm M_{\odot}]'),
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
        plt.hist(galaxies, bins = binnum,  edgecolor = 'black', color = (0,0,0,0), linewidth = 1.5)
        if options.stats:
            # calculates a lot of stats
            mean = numpy.mean(galaxies)
            median = numpy.median(galaxies)
            std = numpy.std(galaxies)
            skew = stats.skew(galaxies, bias = False)
            kurt = stats.kurtosis(galaxies)
            print('mean: ' + str(mean) + '\n' +
            'median: ' + str(median) + '\n' +
            'standard deviation: ' + str(std) + '\n' +
            'skewness: ' + str(skew) + '\n' +
            'kurtosis: ' + str(kurt))
            x = numpy.arange(min(galaxies), max(galaxies), 0.001)
            binwidth = (max(galaxies) - min(galaxies))/binnum
            plt.plot(x, len(galaxies)*binwidth*stats.norm.pdf(x, mean, std), color = 'black')
        pylab.xlabel(name, size = 15)
        pylab.ylabel(r'$N$', size = 15)
        pylab.xticks(size = 15)
        pylab.yticks(size = 15)
        pylab.show()

    # if txt output is wanted
    if options.txt:
        init.print_file = True

    # graph for tracing the mass of an object in a galaxy
    galaxies2 = None
    if options.stellar:
        init.M_stellar = options.stellar
        galaxies2 = trace.Trace(init.file_name).data
    elif options.darkmatter:
        init.M_dm = options.darkmatter
        galaxies2 = trace.Trace(init.file_name).data
    elif options.blackhole:
        init.M_bh = options.blackhole
        galaxies2 = trace.Trace(init.file_name).data

    if galaxies2 is not None:
        if options.data == 'redshift':
            res = [g[0][var] for g in galaxies2]
        else:
            res = [g[1][var] for g in galaxies2]
        # produces scatter plot
        if options.downsizing:
            redshift = [g[0].redshift for g in galaxies2]
            # if black holes, filter out -inf
            if var == 9:
                filt = [g for g in zip(redshift, res) if g[1] != float('-inf')]
                redshift = [g[0] for g in filt]
                res = [g[1] for g in filt]
            pylab.scatter(redshift, res, color = 'b', marker = 'o', s = 16, alpha = 0.3, edgecolors = 'none')
            if options.stats:
                # bin values using a dictionary
                _, binedge = numpy.histogram(redshift, bins = binnum)
                bin_dict = defaultdict(lambda: [])
                for i in list(zip(redshift, res)):
                    bin_mid, val = [((a+b)/2, i[1]) for (a, b) in list(zip(binedge, binedge[1:])) if a <= i[0] <= b][0]
                    bin_dict[bin_mid].append(val)
                # calculate mean lines
                x_mid = [(a+b)/2 for (a, b) in list(zip(binedge, binedge[1:]))]
                red_mid, l, m, u = [], [], [], []
                for i in x_mid:
                    vals = bin_dict[i]
                    # only extend the mean lines if there are more than 30 data points
                    if len(vals) >= 30:
                        red_mid.append(i)
                        l.append(numpy.percentile(vals, 16))
                        m.append(numpy.percentile(vals, 50))
                        u.append(numpy.percentile(vals, 84))
                # plot
                pylab.plot(red_mid, l, label = '16th percentile', color = 'black', linestyle = '--', alpha = 0.7)
                pylab.plot(red_mid, m, label = 'mean', color = 'black', alpha = 0.7)
                pylab.plot(red_mid, u, label = '84th percentile', color = 'black', linestyle = '--', alpha = 0.7)
            pylab.xlabel(r'$z$', size = 15)
            pylab.ylabel(name, size = 15)
            pylab.show()
        # produces histogram
        else:
            # if black holes, filter out -inf
            if var == 9:
                res = [g for g in res if g != float('-inf')]
            plt.hist(res, bins = binnum,  edgecolor = 'black', color = (0,0,0,0), linewidth = 1.5)
            if options.stats:
                # calculates a lot of stats
                mean = numpy.mean(res)
                median = numpy.median(res)
                std = numpy.std(res)
                skew = stats.skew(res)
                kurt = stats.kurtosis(res)
                print('mean: ' + str(mean) + '\n' +
                'median: ' + str(median) + '\n' +
                'standard deviation: ' + str(std) + '\n' +
                'skewness: ' + str(skew) + '\n' +
                'kurtosis: ' + str(kurt))
                x = numpy.arange(min(res), max(res), 0.001)
                binwidth = (max(res) - min(res))/binnum
                plt.plot(x, len(res)*binwidth*stats.norm.pdf(x, mean, std), color = 'black')
            pylab.xlabel(name, size = 15)
            pylab.ylabel(r'$N$', size = 15)
            # pylab.xticks(size = 12)
            # pylab.yticks(size = 12)
            pylab.show()
