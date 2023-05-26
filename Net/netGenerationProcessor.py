import random
import numpy as np
from Net.DeepNet import DeepNet
from Net.Game import Game

class NetGenerationProcessor:
    def __init__(self,count_nets, count_top_nets, count_child, count_w_mutant, count_s_mutant):
        self.count_nets = count_nets
        self.count_top_nets = count_top_nets
        self.count_child = count_child
        self.count_w_mutant = count_w_mutant
        self.count_s_mutant = count_s_mutant

    def fit_loss(self, game, net, iteration):
        loss = 1000
        if game.isAlive:
            count_robot = game.model.office.count_robot
            s = game.model.status
            numerator = ((-1) * s.money * (s.money + s.users * s.loyal * 0.3 - count_robot))
            denominator = iteration * 1000000
            loss = numerator / denominator

        net.model.fit([game.get_state()], [loss], epochs=1, verbose=0)


    def select_top_nets(self, nets): # сортировка сетей по крутости
        fitness = [net.fitness for net in nets]
        elites = [nets[i] for i in np.argsort(fitness)[::-1][:self.count_top_nets]]
        return elites

    # weights in sorted range
    def process(self, weights):
        if not len(weights) == self.count_top_nets:
            raise NameError(len(weights), "- len nets not equal ", self.count_top_nets)
        res = weights.copy()

        #for i in range(int(l_w * 0.1)):
            #res.append(weights[i])
        r = min(self.count_nets-len(res),self.count_nets)
        for i in range(r):
            index1 = random.randint(0, self.count_top_nets - 1)
            index2 = random.randint(0, self.count_top_nets - 1)
            res.append(self.pairing(weights[index1], weights[index2]))

        r = min(self.count_nets-len(res), self.count_w_mutant)
        for i in range(r):
            res.append(self.mutate_net(weights[i].copy()))

        r = min(self.count_nets-len(res), self.count_s_mutant)
        for i in range(r):
            index = random.randint(0, self.count_top_nets - 1)
            res.append(self.mutate_net(weights[index].copy(), 0.5, 0.2))

        counter = 0
        while len(res) < self.count_nets:
            if counter == self.count_top_nets:
                counter = 0
            res.append(weights[counter])
            counter += 1
        if not len(res) == self.count_nets:
            raise NameError("must equal!", len(res), "|", self.count_nets)
        return res

    def pairing(self, parent_net1,  parent_net2):
        res = []
        parent_net1 = parent_net1.copy()
        parent_net2 = parent_net2.copy()
        if not len(parent_net2) == len(parent_net2):
            raise NameError(len(parent1), len(parent2), "not equal len layer nets")

        for layer_i in range(len(parent_net1)):
            if not len(parent_net1[layer_i]) == len(parent_net2[layer_i]):
                raise NameError(len(parent1), len(parent2), "not equal len layer:", layer_i)
            parent_l_1 = parent_net1[layer_i]
            parent_l_2 = parent_net2[layer_i]
            tmp = []

            for i in range(len(parent_l_1)):
                if type(parent_l_1[i]) == np.ndarray:
                    tmp.append(parent_l_1[i])
                    for j in range(len(parent_l_1[i])):
                        tmp[i][j] = (parent_l_1[i][j] if random.random() < 0.5 else parent_l_2[i][j])
                else:
                    tmp.append(parent_l_1[i] if random.random() < 0.5 else parent_l_2[i])

            res.append(np.array(tmp, dtype=np.float32))

        return res

    def mutate_net(self, weights, percent_range=0.05, gen_percent=1.00):
        weights = weights.copy()
        for layer_i in range(len(weights)):
            if random.random() < gen_percent:
                r = (random.random() * 2 - 1) * percent_range
                for j in range(len(weights[layer_i])):
                    weights[layer_i][j] *= (1 + r)
        return weights
