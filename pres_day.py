from read import GalaxyData

class PresentDay (GalaxyData):
    def pres_galaxy(self, key, galaxy):
        pres_key = (0, 1000)
        current_galaxy = galaxy
        # if galaxy doesn't exist in next snapshot
        keys = self.read_data.list_of_keys
        prev_keys = keys[:keys.index(key)]
        for current_key in reversed(prev_keys):
            if current_key == pres_key:
                return current_galaxy
            next_gals = self.read_data.galaxy_data[current_key]
            next_gal = [g for g in next_gals if g.current == current_galaxy.next]
            if len(next_gal) == 0:
                return None
            current_galaxy = next_gal[0]
