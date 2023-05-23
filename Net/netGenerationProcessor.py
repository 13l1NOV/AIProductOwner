import random
import numpy as np

class NetGenerationProcessor:

    def __init__(self):
        self.count_top_nets = 20 # must more than 4
        pass

    def select_top_nets(self, nets): # сортировка сетей по крутости
        fitness = [net.fitness for net in nets]
        elites = [nets[i] for i in np.argsort(fitness)[self.count_top_nets:]]
        return elites
    # nets in sorted range
    # nets = [[]] # поправка weights = [[[w]] [b]] # мы работаем с весами а не с сетью
    def process(self, weights):
        if not len(weights) == self.count_top_nets:
            raise NameError(len(weights), "- len nets not equal ", self.count_top_nets)

        res = []
        for i in range(int(len(weights) * 1.5)):
            index1 = random.randint(0, len(weights) - 1)
            index2 = random.randint(0, len(weights) - 1)
            res.append(self.pairing(weights[index1], weights[index2]))

        for i in range(int(len(weights) * 0.25)):
            res.append(self.mutate_net(weights[i]))

        for i in range(int(len(weights) * 0.25)):
            index = random.randint(len(weights) * 0.25, len(weights) - 1)
            res.append(self.mutate_net(weights[index], 0.5, 0.2))

        if not len(res) == len(weights) * 2:
            raise NameError("must equal!")
        return res

    def pairing(self, parent_net1,  parent_net2):
        res = []
        if not len(parent_net2) == len(parent_net2):
            raise NameError(len(parent1), len(parent2), "not equal len layer nets")

        for layer_i in range(len(parent_net1)):
            if not len(parent_net1[layer_i]) == len(parent_net2[layer_i]):
                raise NameError(len(parent1), len(parent2), "not equal len layer:", layer_i)
            parent_l_1 = parent_net1[layer_i]
            parent_l_2 = parent_net2[layer_i]
            res.append([])
            for i in range(len(parent_l_1)):
                res[layer_i].append(parent_l_1[i] if random.random() < 0.5 else parent_l_2[i])
        return res

    def mutate_net(self, net, percent_range=0.05, gen_percent=1.00):
        for layer_i in range(len(net)):
            mute_gen = random.random() < gen_percent
            if(mute_gen):
                r = (random.random() * 2 - 1) * percent_range
                for j in range(len(net[layer_i])):
                    net[layer_i][j] *= (1 + r)
