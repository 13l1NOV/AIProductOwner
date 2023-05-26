from Net.DeepNet import DeepNet
from Net.Game import Game
from Net.netGenerationProcessor import NetGenerationProcessor
import numpy as np
import tensorflow as tf
class NetProcessor:
    def __init__(self):
        self.net_count = 40
        self.countIteration = 10
        self.ngp = NetGenerationProcessor()

    def net_step(self, net, game):
        state = game.get_state()
        do, index = net.step(state)
        game.execute(do, index)
        #return str(do.value) +" "+(" " if index == None else str(index))+"|"
        return (do.value, ("" if index == None else str(index)))

    def run(self):
        nets = []
        generetions = 100

        for i in range(self.net_count):
            nets.append(DeepNet())

        for generation in range(1, generetions):
            iteration = 0
            games = []
            for i in range(self.net_count):
                games.append(Game())
                nets[i].fitness = 200
            print("generetion " + str(generation))
            while iteration <= self.countIteration + generation // 3 * 2:
                iteration += 1
                #print(games[0])
                lives = 0
                do = []
                for i in range(len(nets)):
                    net = nets[i]
                    if games[i].isAlive:
                        prob = self.net_step(nets[i], games[i])
                        do.append(prob)
                        reward = games[i].get_reward()
                        net.fitness = reward

                        if not games[i].state_changed():
                            #net.fitness = -1000000
                            #weights = self.ngp.mutate_net(nets[i].get_weights(), 1.0, 0.01)
                            #nets[i].replace_net_weight(weights)
                            net.fitness -= 10000
                        #print(games[i].get_state())
                        lives += 1
                        prob = calculate_loss(games[i],iteration)
                        net.model.fit([games[i].get_state()],[prob], epochs=1,verbose=0)
                        if not games[i].isAlive:
                            net.fitness = reward


                    print(int(net.fitness), end="|")
                print()
                print("===================== generation: ", generation, " iteration: ", iteration, " lives:", lives)
                #print("".join(do))
                print(do)

                if lives < 1:
                    break

            self.update_nets(nets)



    def update_nets(self, nets):
        print("########################################!!!!!!!!!!!!")
        new_weights = []
        elites = self.ngp.select_top_nets(nets)
        for elite in elites:
            print(elite.fitness)
        print("---------------------------")
        #print(nets[0].get_weights())
        print("########################################")
        for net in elites:
            new_weights.append(net.get_weights())

        new_weights = self.ngp.process(new_weights)
        c = 0
        #for i in new_weights[0]:
        #    print(i)
        #print(new_weights[0])
        for net in nets:
            net.replace_net_weight(new_weights[c])
            c+=1

def calculate_loss(game,count_iter):
    if not game.isAlive:
        return 1000
    game_office = game.model.office
    game = game.model.status
    return ((-1)*game.money*(game.money + game.users*game.loyal*0.3-game_office.count_robot)) / (count_iter*1000000)




