import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import to_precision

def higher_order_gaussian(x, a0, a1, a2):
    """higher order Gaussian function - 2nd order"""
    return np.exp(a0 + a1*x + a2*x**2)

def pdf(data, height, binmid, name, binwidth):
    '''calculates the mean, median, standard deviation, skewness, and kurtosis of the input data. These values are printed to the screen. A pdf plot is produced.'''
    # calculate stats from original galaxy data
    mean = np.mean(data)
    median = np.median(data)
    std = np.std(data)
    skew = stats.skew(data, bias = False)
    kurt = stats.kurtosis(data)
    # figure text
    str_mean = "$\\langle " + name + " \\rangle = " + str(to_precision.std_notation(mean, 3)) + "$ \n"
    str_std = "$\\sigma = " + str(to_precision.std_notation(std, 3)) + "$ \n"
    str_skew = "$\\mathcal{S} = " + str(to_precision.std_notation(skew, 3)) + "$\n"
    str_kurt = "$\\mathcal{K} = " + str(to_precision.std_notation(kurt, 3)) + "$"
    figure_text = str_mean + str_std + str_skew + str_kurt
    plt.figtext(0.57, 0.72, figure_text, bbox = {'facecolor':'white'}, size = "large")
    # print to terminal
    print('mean = ' + str(mean) + ' h^{-1}')
    print('median = ' + str(median) + ' h^{-1}')
    print('standard deviation = ' + str(std) + ' h^{-1}')
    print('skewness =', skew)
    print('kurtosis =', kurt)
    # calculate and plot PDF
    binmid_offset = [i - mean for i in binmid]
    best_fit, error = curve_fit(higher_order_gaussian, binmid_offset, height)
    fitted_heights = [higher_order_gaussian(i, *best_fit) for i in binmid_offset]
    plt.plot(binmid, fitted_heights, color = 'black')
    # we fit by shifting the distribution to center around 0, but we want to report constants without the mean nonsense in the formula
    a0, a1, a2 = best_fit
    print('a0 =', a0 - a1 * mean + a2 * mean**2)
    print('a1 =', a1 - 2 * a2 * mean)
    print('a2 =', a2)
    
