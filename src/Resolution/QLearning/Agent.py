from Game.Player import Player

class Agent(Player):

    def __init__(self, x, y):
        Player.__init__(self, x, y)

    def get_agent_stats(self):
        k = 0
        s = 0
        t = 0
        if(self.has_key()):
            k = 1
        if(self.has_sword()):
            s = 1
        if(self.has_treasure()):
            t = 1
        return k,s,t

    def set_agent_stats(self, k, s, t):
        self.loose_all_items()
        if(k == 1):
            self.gain_key()
        if(s == 1):
            self.gain_sword()
        if(t == 1):
            self.gain_treasure()
