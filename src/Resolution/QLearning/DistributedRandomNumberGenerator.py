import random

class DRNG():

    def __init__(self):
        self.d = dict()
        self.s = 0

    def add_number(self, i , e):
        if(i in self.d.keys()):
            self.s -= self.d[i]
        self.d[i] = e
        self.s += e

    def get_DRB(self):
        r = random.random()
        ratio = 1.0 / self.s
        temp_dist = 0
        for i in self.d.keys():
            temp_dist += self.d[i]
            if(r / ratio <= temp_dist):
                return i
        return 0
