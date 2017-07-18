import read
import init

#returns the data for the redshift closest to the one given

data = None

def retrieve():
    global key
    redshift = init.redshift
    if redshift is not None:
        keys = read.list_of_keys
        # set initial redshifts
        lower, upper = None, None
        # gets the two redshifts closest to the input redshift
        for i in keys:
            if i.redshift >= redshift:
                upper = i
                lower = keys[keys.index(i) - 1]
                break
        # compares the two redshifts and returns the closest
        if lower.redshift - redshift < upper.redshift - redshift:
            key = lower
        else:
            key = upper
