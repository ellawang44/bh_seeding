import numpy as np
import matplotlib.pyplot as plt

def gaussian(data):
    '''calculates the mean, median, standard deviation, skewness, and kurtosis of the input data. These values are printed to the screen. A gaussian plot is produced.'''
    mean = np.mean(data)
    median = np.median(data)
    std = np.std(data)
    skew = stats.skew(data, bias = False)
    kurt = stats.kurtosis(data)
    figure_text = "$\\langle " + name + " \\rangle: " + str(round_sf(mean, 3)) + "$\n$" + "\\sigma: " + str(round_sf(std, 3)) + '$\n$' + "\\mathcal{S}: " + str(round_sf(skew, 3)) + '$\n$' + "\\mathcal{K} : " + str(round_sf(kurt, 3)) + "$"
    plt.figtext(0.59, 0.68, figure_text, bbox = {'facecolor':'white'}, size = "large")
    print('mean:', mean)
    print('median:', median)
    print('standard deviation:', std)
    print('skewness:', skew)
    print('kurtosis:', kurt)
    x = np.arange(min(data), max(data), 0.001)
    plt.plot(x, len(data)*binwidth*stats.norm.pdf(x, mean, std), color = 'black')
