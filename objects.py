import init
from read import GalaxyData

class Objects (GalaxyData):
    # decides what data to retrieve depending on input
    def __init__(self, read_data):
        super(Objects, self).__init__(read_data)
        M_stellar = init.M_stellar
        M_dm = init.M_dm
        M_bh = init.M_bh
        r = init.r
        if M_stellar is not None:
            var = 7 # stellar mass
            obj = M_stellar
            err = 'stars'
        elif M_dm is not None:
            var = 8 # dark matter mass
            obj = M_dm
            err = 'dark matter haloes'
        elif M_bh is not None:
            var = 9 # black hole mass
            obj = M_bh
            err = 'black holes'
        else:
            var = None

        # takes the redshifts for the chosen object
        if var is not None:
            objects = []
            for key, value in self.read_data.galaxy_data.items():
                current_redshift = key.redshift
                counts = 0
                # gets the number of objects that satisfy the given mass range
                for galaxy in value:
                    if obj - r < galaxy[var] < obj + r:
                        counts += 1
                # build a tuple of the redshift and number if there is more than 0 objects that satisfy the mass range
                if counts != 0:
                    objects.append((current_redshift, counts))
            # if there are objects that satisfy the given mass range
            # gets the data ready for plotting
            if objects != []:
                redshift = []
                num = []
                # sadly the redshifts aren't sorted because dictionaries aren't sorted
                for i in sorted(objects):
                    redshift.append(i[0])
                    num.append(i[1])
                self.data = (redshift, num)
            else:
                raise ValueError('no ' + err + ' found within mass range ' + str(obj - r) + ' to ' + str(obj + r))
