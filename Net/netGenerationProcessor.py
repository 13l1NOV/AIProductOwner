import random
import numpy as np
from Net.DeepNet import DeepNet
from Net.Game import Game

class NetGenerationProcessor:
    def __init__(self):
        self.count_top_nets = 20 # must more than 10

    def fit_loss(self, game, net, iteration):
        los = 1000
        if game.isAlive:
            count_robot = game.model.office.count_robot
            s = game.model.status
            numerator = ((-1) * s.money * (s.money + s.users * s.loyal * 0.3 - count_robot))
            denominator = iteration * 1000000
            los = numerator / denominator

        net.model.fit([game.get_state()], [los], epochs=1, verbose=0)


    def select_top_nets(self, nets): # сортировка сетей по крутости
        fitness = [net.fitness for net in nets]
        elites = [nets[i] for i in np.argsort(fitness)[::-1][:self.count_top_nets]]
        return elites

    # weights in sorted range
    def process(self, weights):
        if not len(weights) == self.count_top_nets:
            raise NameError(len(weights), "- len nets not equal ", self.count_top_nets)

        weights = weights.copy()
        res = []
        l_w = len(weights)

        for i in range(int(l_w * 0.1)):
            res.append(weights[-i])

        for i in range(int(l_w * 1.4)):
            index1 = random.randint(0, l_w - 1)
            index2 = random.randint(0, l_w - 1)
            res.append(self.pairing(weights[index1], weights[index2]))

        for i in range(int(l_w * 0.1), int(l_w * 0.3)):
            res.append(self.mutate_net(weights[i]))

        for i in range(int(l_w * 0.3)):
            index = random.randint(l_w * 0.3, l_w - 1)
            res.append(self.mutate_net(weights[index], 0.5, 0.2))

        if not len(res) == l_w * 2:
            raise NameError("must equal!", len(res), "|", l_w)
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
    #
    # def rework_weights(self, weights, gen_percent=1.00):
    #     weights = weights.copy()
    #     for layer_i in range(len(weights)):
    #         mute_gen = random.random() < gen_percent
    #         if(mute_gen):
    #             r = (random.random() * 2 - 1)
    #             for j in range(len(weights[layer_i])):
    #                 if type(weights[layer_i][j]) == np.ndarray:
    #                     for k in range(len(weights[layer_i][j])):
    #                         weights[layer_i][j][k] = float(r)
    #                 else:
    #                     weights[layer_i][j] = float(r)
    #     return weights
    #
    # def mutate_net2(self, weights, mutation_rate=0.5, mutation_size=0.001):
    #     mutated_weights = np.copy(weights)
    #     for i, weight in enumerate(mutated_weights):
    #         if np.random.random() < mutation_rate:
    #             mutated_weights[i] += np.random.normal(loc=0.0, scale=mutation_size)
    #     return mutated_weights
    #
    # def mutate_net_new(self):
    #     net = DeepNet()
    #     state = Game()
    #     state = state.get_state()
    #     net.step(state)
    #     weights = net.model.get_weights()
    #     return weights
