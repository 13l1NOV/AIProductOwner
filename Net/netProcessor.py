from Net.DeepNet import DeepNet
from Net.Game import Game

class NetProcessor:
    def __init__(self):
        self.net_count = 40
        self.countIteration = 800
        pass

    def net_step(self, net, game):
        state = game.get_state()
        do, index = net.step(state)
        game.execute(do, index)

    def run(self):
        nets = []
        games = []

        for i in range(self.net_count):
            nets.append(DeepNet())
            games.append(Game())

        for net in nets:
            net.fitness = 200

        iteration = 0
        while iteration <= self.countIteration:
            print("iteration=======================")
            print(games)
            for i in range(len(nets)):
                self.net_step(nets[i], games[i])
                #games[i] is alive

        self.update_nets(nets, games)

    def update_nets(self, nets, games):
        pass

