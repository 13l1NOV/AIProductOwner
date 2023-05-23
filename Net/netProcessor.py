from Net.DeepNet import DeepNet
from Net.Game import Game
from Net.netGenerationProcessor import NetGenerationProcessor
import numpy as np
class NetProcessor:
    def __init__(self):
        self.net_count = 40
        self.countIteration = 2
        self.ngp = NetGenerationProcessor()

    def net_step(self, net, game):
        state = game.get_state()
        do, index = net.step(state)
        game.execute(do, index)

    def run(self):
        nets = []
        games = []
        generetions = 100

        for i in range(self.net_count):
            nets.append(DeepNet())
            games.append(Game())

        for net in nets:
            net.fitness = 200

        for generation in range(1, generetions):
            iteration = 0
            games = []
            for i in range(self.net_count):
                games.append(Game())
            print("generetion "+ str(generation))
            print("generetion " + str(generation))
            print("generetion " + str(generation))
            print("generetion " + str(generation))
            while iteration <= self.countIteration:
                iteration+=1
                print("iteration=======================")
                #print(games[0])
                lives = 0
                for i in range(len(nets)):
                    if games[i].isAlive:
                        self.net_step(nets[i], games[i])
                        print(games[i].get_state())
                        lives += 1
                        net.fitness = games[i].get_reward()

                if lives < 1:
                    break

            self.update_nets(nets)



    def update_nets(self, nets):
        print("########################################")
        print("########################################")
        print("########################################")
        new_weights = []
        elites = self.ngp.select_top_nets(nets)
        print(nets[0].get_weights())
        print("########################################")
        for net in elites:
            new_weights.append(net.get_weights())

        new_weights = self.ngp.process(new_weights)
        c = 0
        print(new_weights[0])
        for net in nets:
            net.replace_net_weight(new_weights[c])
            c+=1







