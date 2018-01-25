import init
import history
from read import GalaxyData

class Trace (GalaxyData):
    # considers the galaxy mergers that occur and returns either redshift, stellar mass, black hole mass or dark matter halo mass when the given object first crosses the given mass (called threshold here)
    # except treats dark matter halo slightly differently. The dark matter halo is not monotomically increasing due to the friends of friends halo finder. We take the range over which it crosses the threshold mass and pick the snapshot in the middle

    def __init__(self, read_data):
        super(Trace, self).__init__(read_data)
        keys = self.read_data.list_of_keys
        objects = []
        if init.M_stellar is not None:
            var = 7 # stellar mass
            obj = init.M_stellar
            err = 'stars'
            file_name = 'star'
        elif init.M_dm is not None:
            var = 8 # dark matter mass
            obj = init.M_dm
            err = 'dark matter halos'
            file_name = 'dm'
        elif init.M_bh is not None:
            var = 9 # black hole mass
            obj = init.M_bh
            err = 'black holes'
            file_name = 'bh'
        elif init.M_g is not None:
            var = 10 # gas mass
            obj = init.M_g
            err = 'gas'
            file_name = 'gas'
        else:
            var = None

        # print file containing snapshots and galaxy numbers
        if init.print_file:
            f = open(file_name + '_mass_' + str(int(obj)) + '.txt', 'w')
            f.write('snapshot \t galaxy number \n')
        hist = history.History(self.read_data)
        # if black hole mass, then it is monotonically increasing
        if var == 9:
            for key in keys:
                for galaxy in self.read_data.galaxy_data[key]:
                    prev_galaxy = hist.m_preimage(key, galaxy)
                    if prev_galaxy is not None and prev_galaxy[var] < obj < galaxy[var]:
                        objects.append((key, galaxy))
                        if init.print_file:
                            f.write(str(int(key.snapshot)) + ' \t ' + str(int(galaxy.current)) + ' \n')
        else:
            for galaxy in self.read_data.galaxy_data[(2.2336349, 700)]:
                evos = hist.evolution(keys[0], galaxy, [])
                midpoints = [hist.midpoint(evo, obj, var) for evo in evos]
                frames = [f for f in midpoints if f is not None]
                # remove doubles
                if frames != []:
                    for fra in frames:
                        objects.append(fra)
                        if init.print_file:
                            f.write(str(int(fra[0].snapshot)) + '\t' + str(int(fra[1].current)) + '\n')

        # gotta close the file so Probie's computer (and Windows) doesn't get annoyed
        if init.print_file:
            f.close()

        if objects != []:
            self.data = objects
        else:
            raise ValueError('no ' + err + ' found at the given mass')
