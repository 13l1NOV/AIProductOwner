import random

class NetGenerationProcessor:

    def __init__(self):
        self.count_top_nets = 20 # must more than 4
        pass

    # nets in sorted range
    # nets = [[]]
    def process(self, nets):
        if not len(nets) == self.count_top_nets:
            raise NameError(len(nets), "- len nets not equal ", self.count_top_nets)

        res = []
        for i in range(nets * 1.5):
            index1 = random.randint(0, len(nets) - 1)
            index2 = random.randint(0, len(nets) - 1)
            res.append(self.pairing(nets[index1], nets[index2]))

        for i in range(nets * 0.25):
            res.append(mutate_array(nets[i]))

        for i in range(nets * 0.25):
            index = random.randint(nets * 0.25, len(nets) - 1)
            res.append(self.mutate_net(nets[index], 0.5, 0.2))

        if not len(res) == len(nets) * 2:
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
