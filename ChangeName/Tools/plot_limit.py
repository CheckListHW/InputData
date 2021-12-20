class PlotLimit:
    def __init__(self, x, y=None, z=None):
        self.x, self.y, self.z = x, y, z

    def get_max_limit(self):
        limits = [x for x in [self.x, self.z, self.z] if x]
        if len(limits) == 0:
            return None
        return max(limits)
