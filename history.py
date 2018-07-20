from read import GalaxyData

class History (GalaxyData):
    def m_preimage(self, key, galaxy):
        # get the biggest galaxy in the preimage of the input galaxy
        keys = self.read_data.list_of_keys
        if key == keys[-1]:
            return None
        else:
            prev_galaxys = [prev_galaxy for prev_galaxy in self.read_data.galaxy_data[keys[keys.index(key)+1]] if galaxy.previous == prev_galaxy.current]
            if prev_galaxys == []:
                return None
            else:
                return prev_galaxys[0]

    def m_evolution(self, key, galaxy, threshold, var):
        # traces the evolution of 1 galaxy only. It will return a list of tuples where each tuple describes the galaxy at a different snapshot in reverse chronological order
        # I mean technically could've been written only to work for the present day snapshot galaxies, it would've been easier, but that's no fun c:
        # traces the biggest galaxy if a merger occurs
        keys = self.read_data.list_of_keys
        # set initial condition
        galaxy_list = []
        current_galaxy = galaxy
        first = None # first time the mass crosses the threshold
        # a list of keys that come after the given key in the list
        next_keys = keys[keys.index(key):]
        for current_key in next_keys:
            prev_galaxy = self.m_preimage(current_key, current_galaxy)
            if prev_galaxy is None:
                if first is not None:
                    galaxy_list.append((current_key, current_galaxy))
                    break
                else:
                    break
            else:
                if first is None:
                    if prev_galaxy[var] < threshold < current_galaxy[var]:
                        first = (current_key, current_galaxy)
                        last = (keys[keys.index(current_key) + 1], prev_galaxy)
                        galaxy_list.append((current_key, current_galaxy))
                else:
                    galaxy_list.append((current_key, current_galaxy))
                    if prev_galaxy[var] < threshold < current_galaxy[var]:
                        last = (keys[keys.index(current_key) + 1], prev_galaxy)
            current_key = keys[keys.index(current_key) + 1]
            current_galaxy = prev_galaxy
        if galaxy_list == []:
            return None
        else:
            region = galaxy_list[:(galaxy_list.index(last)+1)]
            return region

    def preimage(self, key, galaxy, check = False):
        # get previous galaxies that are the pre image of the input galaxy
        keys = self.read_data.list_of_keys
        if key == keys[-1]:
            return []
        else:
            # index 0 returns current number, 1 returns next number
            galaxies = [prev_galaxy for prev_galaxy in self.read_data.galaxy_data[keys[keys.index(key)+1]] if galaxy.current == prev_galaxy.next]
            if check and len(galaxies) == 0:
                print('lost galaxy')
            return galaxies

    def evolution(self, key, galaxy, prev_evo):
        # traces the history of a galaxy. It will return a list of tuples where each tuple describes the galaxy at a different snapshot in reverse chronological order
        keys = self.read_data.list_of_keys
        # base conditions
        try:
            prev_key = keys[keys.index(key) + 1]
        except IndexError: return [prev_evo]
        prev_gals = self.preimage(key, galaxy)
        prev_evo.append((key, galaxy))
        while len(prev_gals) < 2:
            if len(prev_gals) == 0:
                return [prev_evo]
            else:
                # allows us to call evolution less times than otherwise if this was placed outside the while loop
                prev_evo.append((prev_key, prev_gals[0]))
                galaxy = prev_gals[0]
                key = prev_key
                try:
                    prev_key = keys[keys.index(key) + 1]
                except IndexError: return [prev_evo]
                prev_gals = self.preimage(key, galaxy)
                #evolution(prev_key, prev_gals[0], prev_evo)
        # if there is more than 1 previous galaxy
        result = []
        m_prev_gal = [g for g in prev_gals if g.current == galaxy.previous][0]
        result.extend(self.evolution(prev_key, m_prev_gal, prev_evo))
        prev_gals.remove(m_prev_gal)
        for gal in prev_gals:
            result.extend(self.evolution(prev_key, gal, []))
        return result

    def midpoint(self, gal_evo, threshold, var):
        # takes the midpoint of the section of the list that crosses the threshold
        galaxy = gal_evo[0][1]
        cross = [n for n,(cg,pg) in enumerate(zip(gal_evo,gal_evo[1:])) if cg[1][var] > threshold > pg[1][var]]
        if len(cross) == 0:
            #if gal_evo[-1][0][1] < 500:
                #print(gal_evo[-1][0],gal_evo[-1][1][2])
            # if they cross the threshold 0 times, then they are either above the threshold already or have never reached the threshold
            if gal_evo[-1][1][var] > threshold:
                return None#gal_evo[-1]
            else:
                return None
        if len(cross) == 1:
            # if they cross the threshold 1 times, then we should get the snapshot where it crosses the threshold.
            return gal_evo[cross[0]]
        else:
            first, last = cross[0], cross[-1]
            # since mass can go down below the threshold, if this occurs in present day, we include it in the region (it'll eventually go back up)
            if galaxy[var] < threshold:
                region = gal_evo[:(last+2)]
            else:
                region = gal_evo[first:last+2]
            mid = len(region) / 2
            if mid.is_integer():
                return region[int(mid)]
            else:
                lower = region[int(mid) - 1]
                upper = region[int(mid)]
                if region[-1][0].redshift - lower[0].redshift < upper[0].redshift - region[0][0].redshift:
                    return lower
                else:
                    return upper
