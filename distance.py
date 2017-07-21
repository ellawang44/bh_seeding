from read import GalaxyData

class Distance (GalaxyData):
    def s5(self, key, galaxy):
        galaxies = [(self.distance(gal, galaxy), gal) for gal in self.read.galaxy_data[key] if gal != galaxy]
        galaxies.sort()
        # if I just take the 5th element and it doesn't exist here, would it still return None? I mean it currently returns None like this but it would make it run faster, not that it matters I'm probably going to change this anyway
        min5 = galaxies[:5]
        if len(min5) == 5:
            return min5[-1][0]
        # try a nontrivial method when you get better
        '''
        for gal in galaxies:
            d = distance(gal, galaxy)
            if min5 == []:
                min5.append((gal, d))
            else:
                # this is not Haskell. feelsbadman
                n_min5 = []
                flag = False
                for g in min5:
                    if not flag and d < g[1]:
                        n_min5.append((gal, d))
                        flag = True
                    n_min5.append(g)
                min5 = n_min5[:5]
        if len(min5) == 5:
            return min5[-1][1]
            '''

    def distance(self, gal, galaxy):
        sim_box_size = 25000/0.7 # magic numbers ftw
        x = abs(gal.xcoord - galaxy.xcoord)
        y = abs(gal.ycoord - galaxy.ycoord)
        z = abs(gal.zcoord - galaxy.zcoord)
        dist = numpy.sqrt(min(x, sim_box_size - x)**2 + min(y, sim_box_size - y)**2 + min(z, sim_box_size - z)**2)
        return dist
