import init
import history
from read import GalaxyData

class Trace (GalaxyData):
    # considers the galaxy mergers that occur and returns either redshift, stellar mass, black hole mass or dark matter halo mass when the given object first crosses the given mass (called threshold here)
    # except treats dark matter halo slightly differently. The dark matter halo is not monotomically increasing due to the friends of friends halo finder. We take the range over which it crosses the threshold mass and pick the snapshot in the middle

    def __init__(self,name):
        super(Trace, read_data).__init__(read_data)
        keys = self.read_data.list_of_keys
        objects = []
        if init.M_stellar is not None:
            var = 7 # stellar mass
            obj = init.M_stellar
            err = 'stars'
        elif init.M_dm is not None:
            var = 8 # dark matter mass
            obj = init.M_dm
            err = 'dark matter haloes'
        elif init.M_bh is not None:
            var = 9 # black hole mass
            obj = init.M_bh
            err = 'black holes'
        else:
            var = None

        # print file containing snapshots and galaxy numbers
        if init.print_file:
            f = open(str(err) + ' of mass ' + str(int(obj)) + '.txt', 'w')
            f.write('snapshot \t galaxy number \n')
        hist = history.History(self.read_data)
        # if black hole mass, then it is monotonically increasing
        if var == 9:
            for key in keys:
                for galaxy in self.read_data.galaxy_data[key]:
                    prev_galaxy = hist.m_preimage(key, galaxy)
                    # decide what to append
                    if init.item == 'stellar':
                        item = galaxy.stellar_mass
                    elif init.item == 'dark matter':
                        item = galaxy.dark_matter_mass
                    elif init.item == 'black hole':
                        item = galaxy.black_hole_mass
                    else:
                        item = key.redshift
                    if prev_galaxy is not None and prev_galaxy[var] < obj < galaxy[var]:
                        objects.append(item)
                        if init.print_file:
                            f.write(str(int(key.snapshot)) + ' \t ' + str(int(galaxy.current)) + ' \n')
        else:
            for galaxy in self.read_data.galaxy_data[keys[0]]:
                frame = (hist.midpoint(keys[0], galaxy, obj, var))
                if frame is not None:
                    if init.item == 'stellar':
                        objects.append(frame[1].stellar)
                    elif init.item == 'dark matter':
                        objects.append(frame[1].dark_matter_mass)
                    elif init.item == 'black hole':
                        objects.append(frame[1].black_hole_mass)
                    else:
                        objects.append(frame[0].redshift)
                    if init.print_file:
                        f.write(str(int(frame[0].snapshot)) + '\t' + str(int(frame[1].current)) + '\n')

        # gotta close the file so Probie's computer (and Windows) doesn't get annoyed
        if init.print_file:
            f.close()

        if objects != []:
            data = objects
        else:
            raise ValueError('no ' + err + ' found at the given mass')
