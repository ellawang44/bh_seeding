from read import GalaxyData

class Present (GalaxyData):
    def present(self, key, galaxy):
        # get the present day image of the input galaxy
        keys = self.read_data.list_of_keys
        pres_key = keys[0]
        keys = list(reversed(keys))
        rem_keys = keys[keys.index(key)+1:]
        current_galaxy = galaxy
        for k in rem_keys:
            next_gals = [next_gal for next_gal in self.read_data.galaxy_data[k] if next_gal.current == current_galaxy.next]
            if next_gals == []:
                return None
            current_galaxy = next_gals[0]
            if k == pres_key:
                return current_galaxy
