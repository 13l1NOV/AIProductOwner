from Net.DeepNet import DeepNet
from Net.Game import Game
from Net.netGenerationProcessor import NetGenerationProcessor
import numpy as np
import tensorflow as tf

class NetProcessor:
    def __init__(self):
        self.net_count = 40
        self.ngp = NetGenerationProcessor()

    def net_step(self, net, game):
        state = game.get_state()
        do, index = net.step(state)
        game.execute(do, index)
        return (do, index)

    def formatDoing(self, do, index):
        return (do.value, ("" if index == None else str(index)))

    def run(self, generetions=100, iterations=30):
        nets = []

        for i in range(self.net_count):
            nets.append(DeepNet())

        for generation in range(1, generetions):
            iteration = 0
            games = []

            for i in range(self.net_count):
                games.append(Game())
                nets[i].fitness = 200

            print("generetion " + str(generation))
            while iteration <= iterations:# + generation // 3 * 2:
                iteration += 1
                lives = 0
                net_doings = []

                print("Fitness net i after predict:|", end="")
                for i in range(len(nets)):
                    net = nets[i]
                    if games[i].isAlive:
                        lives += 1

                        do, index = self.net_step(nets[i], games[i])
                        net_doings.append(self.formatDoing(do, index))
                        reward = games[i].get_reward()
                        net.fitness = reward

                        if not games[i].state_changed():
                            #weights = self.ngp.mutate_net(nets[i].get_weights(), 1.0, 0.01)
                            #nets[i].replace_net_weight(weights)
                            net.fitness -= 10000

                        self.ngp.fit_loss(games[i], net, iteration)
                        # if not games[i].isAlive: # ЗАЧЕМ ЭТО НАДО БЫЛО ??? НЕСКОЛЬКО СТРОК ВЫШЕ УЖЕ УСТАНАВЛИВАЛАСЬ НАГРАДА
                        #     net.fitness = reward
                        print(int(net.fitness), end="|")

                print("\n===================== generation: ", generation, " iteration: ", iteration, " lives:", lives)
                print("Действия сетей-(enum id, index)", net_doings)

                if lives < 1:
                    break

            # after generation
            self.update_nets(nets)

    def update_nets(self, nets):
        print("=======================================")
        was_weights = []
        elites = self.ngp.select_top_nets(nets)

        print("best nets fitness:", end="")
        for net in elites:
            print(net.fitness, end="|")
            was_weights.append(net.get_weights())
        print("\n=======================================")

        new_weights = self.ngp.process(was_weights)

        for i in range(len(nets)):
            nets[i].replace_net_weight(new_weights[i])