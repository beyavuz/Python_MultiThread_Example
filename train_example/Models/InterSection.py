# kavşak, köşeler
class Intersection:
    def __init__(self, uid, mutex, locked_by):
        self.uid = uid
        self.mutex = mutex
        self.locked_by = locked_by  # hangi train lock'u almış.Kavşaktaki locku hangi train almış.
