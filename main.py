import read
import trace
import redshift
import snapshot
import distance
import present
import pylab
import init
import numpy
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats
from optparse import OptionParser
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

exec(b'\xe4\xb9\x87\xe4\xb9\x82\xe3\x84\x92\xe5\xb0\xba\xe5\x8d\x82\xe3\x84\x92\xe5\x8d\x84\xe4\xb8\xa8\xe5\x8c\x9a\xe5\x8c\x9a'.decode('utf-8') + ' = "large"')

parser = OptionParser()

# ks test keromerogh's speamouth test?
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
parser.add_option('-m', '--stellar', type = 'float', dest = 'stellar', help = 'Sets the threshold stellar mass, galaxies that just pass above that threshold mass will be recorded. Use "--data" to determine what aspect of those galaxies to histogram. Use "--xaxis" and "--yaxis" to plot a scatter plot of chosen data for each axis. Use "--txt" to output a txt file containing the galaxy number of the galaxies that just pass above the threshold mass and the snapshot at which it occurs.')

parser.add_option('-d', '--darkmatter', type = 'float', dest = 'darkmatter', help = 'Sets the threshold dark matter halo mass, galaxies that just pass above that threshold mass will be recorded. Use "--data" to determine what aspect of those galaxies to histogram. Use "--xaxis" and "--yaxis" to plot a scatter plot of chosen data for each axis. Use "--txt" to output a txt file containing the galaxy number of the galaxies that just pass above the threshold mass and the snapshot at which it occurs.')

parser.add_option('-b', '--blackhole', type = 'float', dest = 'blackhole', help = 'Sets the threshold black hole mass, galaxies that just pass above that threshold mass will be recorded. Use "--data" to determine what aspect of those galaxies to histogram. Use "--xaxis" and "--yaxis" to plot a scatter plot of chosen data for each axis. Use "--txt" to output a txt file containing the galaxy number of the galaxies that just pass above the threshold mass and the snapshot at which it occurs.')

parser.add_option('-g', '--gas', type = 'float', dest = 'blackhole', help = 'Sets the threshold gas mass, galaxies that just pass above that threshold mass will be recorded. Use "--data" to determine what aspect of those galaxies to histogram. Use "--xaxis" and "--yaxis" to plot a scatter plot of chosen data for each axis. Use "--txt" to output a txt file containing the galaxy number of the galaxies that just pass above the threshold mass and the snapshot at which it occurs.')

# takes the present day s5 data for the galaxies of interest
parser.add_option('--s5', action = 'store_true', dest = 's5', help = 'Takes the selected data and outputs a scatter plot of the mass (object selected with the "--data" flag) along the x-axis and the data on the present day s5 distance. Used together with "--data" and either "--stellar", "--darkmatter" or "--blackhole".')

# determines what to plot on the x and y axis for the galaxies of interest
parser.add_option('-x', '--xaxis', type = 'string', dest = 'xaxis', help = 'Determines what to plot on the x-axis for the galaxy of interst. Used with "-stellar", "--darkmatter", "--blackhole", and "--gas".')

parser.add_option('-y', '--yaxis', type = 'string', dest = 'yaxis', help = 'Determines what to plot on the y-axis for the galaxy of interst. Used with "-stellar", "--darkmatter", "--blackhole", and "--gas".')

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
    vartable = { 'redshift' : (0, 'z'),
                 'xcoord' : (4, 'x-coordinates'),
                 'ycoord' : (5, 'y-coordinates'),
                 'zcoord' : (6, 'z-coordinates'),
                 'stellar' : (7, r'log $M_{*}$ [\rm{M}_{\odot}]'),
                 'dark matter' : (8, r'log $M_{\rm DM}$ [\rm{M}_{\odot}]'),
                 'black hole' : (9, r'log $M_{\rm BH}$ [\rm M_{\odot}]'),
                 'gas' : (10, r'log $M_{\rm g}$ [\rm M_{\odot}]'),
                 None : (None, None)
            }
    var, name = vartable[options.data]
    xvar, xname = vartable[options.xaxis]
    yvar, yname = vartable[options.yaxis]

    # define a sig fig rounding fuction
    def round_sf(x, n):
        return float(('%.' + str(int(n)) + 'g') %  x)

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
        height, binedge = numpy.histogram(galaxies, bins = binnum)
        binwidth = (max(galaxies) - min(galaxies))/binnum
        error = [numpy.sqrt(i) for i in height]
        plt.bar(binedge[:-1], height, width = binwidth, align = 'edge', yerr = error, edgecolor = 'black', color = (0,0,0,0), linewidth = 1.5)
        if options.stats:
            # calculates a lot of stats
            mean = numpy.mean(galaxies)
            median = numpy.median(galaxies)
            std = numpy.std(galaxies)
            skew = stats.skew(galaxies, bias = False)
            kurt = stats.kurtosis(galaxies)
            plt.figtext(0.63, 0.71, r'$\langle$' + name + r'\rangle' + ': ' + str(round_sf(mean, 3)) + '\n' + r'$\sigma$: ' + str(round_sf(std, 3)) + '\n' + r'$\mathcal{S}$: ' + str(round_sf(skew, 3)) + '\n' + r'$\mathcal{K}$: ' + str(round_sf(kurt, 3)), bbox = {'facecolor':'white'}, size = 乇乂ㄒ尺卂ㄒ卄丨匚匚)
            print('mean: ' + str(mean) + '\n' + 'median: ' + str(median) + '\n' + 'standard deviation: ' + str(std) + '\n' + 'skewness: ' + str(skew) + '\n' + 'kurtosis: ' + str(kurt))
            x = numpy.arange(min(galaxies), max(galaxies), 0.001)
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
    elif options.gas:
        init.M_g = options.gas
        galaxies2 = trace.Trace(init.file_name).data

    if galaxies2 is not None:
        # determines the mass data to take if producing histogram
        if options.data:
            if options.data == 'redshift':
                res = [g[0][var] for g in galaxies2]
            else:
                res = [g[1][var] for g in galaxies2]

        # produces scatter plot
        if options.xaxis and options.yaxis:
            if options.xaxis == 'redshift':
                xaxis = [g[0].redshift for g in galaxies2]
            else:
                xaxis = [g[1][xvar] for g in galaxies2]
            if options.yaxis == 'redshift':
                yaxis = [g[0].redshift for g in galaxies2]
            else:
                yaxis = [g[1][yvar] for g in galaxies2]
            # black holes can have mass of -inf
            if xvar == 9:
                xaxis,yaxis = zip(*[(x, y) for (x, y) in zip(xaxis, yaxis) if x != float('-inf')])
            if yvar == 9:
                xaxis,yaxis = zip(*[(x, y) for (x, y) in zip(xaxis, yaxis) if y != float('-inf')])
            pylab.scatter(xaxis, yaxis, color = 'b', marker = 'o', s = 16, alpha = 0.3, edgecolors = 'none')
            if options.stats:
                # bin values using a dictionary
                _, binedge = numpy.histogram(xaxis, bins = binnum)
                bin_dict = defaultdict(lambda: [])
                for i in list(zip(xaxis, yaxis)):
                    bin_mid, val = [((a+b)/2, i[1]) for (a, b) in list(zip(binedge, binedge[1:])) if a <= i[0] <= b][0]
                    bin_dict[bin_mid].append(val)
                # calculate mean lines
                mid = [(a+b)/2 for (a, b) in list(zip(binedge, binedge[1:]))]
                x_mid, l, m, u = [], [], [], []
                for i in mid:
                    vals = bin_dict[i]
                    # only extend the mean lines if there are more than 30 data points
                    if len(vals) >= 30:
                        x_mid.append(i)
                        l.append(numpy.percentile(vals, 16))
                        m.append(numpy.percentile(vals, 50))
                        u.append(numpy.percentile(vals, 84))
                # plot
                pylab.plot(x_mid, l, label = '16th percentile', color = 'black', linestyle = '--', alpha = 0.7)
                pylab.plot(x_mid, m, label = 'mean', color = 'black', alpha = 0.7)
                pylab.plot(x_mid, u, label = '84th percentile', color = 'black', linestyle = '--', alpha = 0.7)
            pylab.xlabel(xname, size = 15)
            pylab.ylabel(yname, size = 15)
            pylab.show()

        # produces s5 scatter plots
        elif options.s5:
            # initiate files
            present = present.Present(init.file_name)
            distance = distance.Distance(init.file_name)
            # find the present day galaxy of the galaxies of interest
            pres_day_gal = [present.present(gal[0], gal[1]) for gal in galaxies2]
            # filter out all the galaxies that don't exist present day anymore
            galaxies = [(pres_gal, gal) for (pres_gal, gal) in zip(pres_day_gal, galaxies2) if pres_gal is not None]
            pres_gals = [gal[0] for gal in galaxies]
            gals = [gal[1] for gal in galaxies]
            # get the s5 distance of the present day galaxies
            s5 = [distance.s5((0, 1000), gal) for gal in pres_gals]
            # filter out all the galaxies that don't have an s5 distance
            data = [(gal, s5_dist) for (gal, s5_dist) in zip(gals, s5) if s5_dist is not None]
            s5 = [d[1] for d in data]
            if var == 0:
                mass_object = [d[0][0][var] for d in data]
            else:
                mass_object = [d[0][1][var] for d in data]
            if var == 9:
                data = [(mass, s5_dist) for (mass, s5_dist) in zip(mass_object, s5) if mass != float('-inf')]
                s5 = [d[1] for d in data]
                mass_object = [d[0] for d in data]
            # plot
            pylab.scatter(mass_object, s5, color = 'b', marker = 'o', s = 16, alpha = 0.3, edgecolors = 'none')
            pylab.xlabel(name, size = 15)
            pylab.ylabel('s5', size = 15)
            pylab.show()

        # produces histogram
        else:
            # if black holes, filter out -inf
            if var == 9:
                res = [g for g in res if g != float('-inf')]
            height, binedge = numpy.histogram(res, bins = binnum)
            binwidth = (max(res) - min(res))/binnum
            error = [numpy.sqrt(i) for i in height]
            plt.bar(binedge[:-1], height, width = binwidth, align = 'edge', yerr = error, edgecolor = 'black', color = (0,0,0,0), linewidth = 1.5)
            if options.stats:
                # calculates a lot of stats
                mean = numpy.mean(res)
                median = numpy.median(res)
                std = numpy.std(res)
                skew = stats.skew(res)
                kurt = stats.kurtosis(res)
                plt.figtext(0.63, 0.71, r'$\langle$' + name + r'\rangle' + ': ' + str(round_sf(mean, 3)) + '\n' + r'$\sigma$: ' + str(round_sf(std, 3)) + '\n' + r'$\mathcal{S}$: ' + str(round_sf(skew, 3)) + '\n' + r'$\mathcal{K}$: ' + str(round_sf(kurt, 3)), bbox = {'facecolor':'white'}, size = 乇乂ㄒ尺卂ㄒ卄丨匚匚)
                print('mean: ' + str(mean) + '\n' + 'median: ' + str(median) + '\n' + 'standard deviation: ' + str(std) + '\n' + 'skewness: ' + str(skew) + '\n' + 'kurtosis: ' + str(kurt))
                x = numpy.arange(min(res), max(res), 0.001)
                plt.plot(x, len(res)*binwidth*stats.norm.pdf(x, mean, std), color = 'black')
            pylab.xlabel(name, size = 15)
            pylab.ylabel(r'$N$', size = 15)
            pylab.show()
