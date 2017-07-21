import init
from read import GalaxyData

class Redshift (GalaxyData):
    #returns the data for the redshift closest to the one given
    def __init__(self, read_data):
        super(Redshift, self).__init__(read_data)
        redshift = init.redshift
        if redshift is not None:
            keys = self.read_data.list_of_keys
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
                self.key = lower
            else:
                self.key = upper
