#from View.view import View
#from Game.game import Game
from Model.model import Model
from Controllers.mainController import Controller
from Net.actor import Actor
import random
import numpy as np
import neat
from Net.net import run_generation
"""
if __name__ == '__main2__':
    model = Model()
    view = View()
    controller = Controller(model)

    print("---------------------")
    status_bar(model)
    status_office(model)
    status_task(model)
    print("---------------------")
    controller.buy_robot(0)
    print("---------------------")
    status_bar(model)
    status_office(model)
    status_task(model)
    print("---------------------")
    controller.buy_robot(0)
    print("---------------------")
    status_bar(model)
    status_office(model)
    status_task(model)
    print("---------------------")
    model.status.money = 1000000

    print("---------------------")
    status_bar(model)
    status_office(model)
    status_task(model)
    print("---------------------")
    controller.create_two_easy_task()
    print("---------------------")
    status_bar(model)
    status_office(model)
    status_task(model)
    print("---------------------")
    controller.move_task_to_selected_list(0)
    # controller.move_task_to_selected_list(1)

    print("---------------------")
    status_bar(model)
    status_office(model)
    status_task(model)
    print("---------------------")
    controller.decomposition_tasks()
    controller.move_subtask_to_selected_list(0)

    print("---------------------")
    status_bar(model)
    status_office(model)
    status_task(model)
    status_subtask(model)
    print("---------------------")

    controller.start_sprint()

    print("---------------------")
    status_bar(model)
    status_office(model)
    status_task(model)
    status_subtask(model)
    print("---------------------")
"""


if __name__ == "__main__":
    #game = Game()
    #game.start()

    #input()
    print("starting")
    generation = 0
    res = np.random.uniform(2, 6)
    res = random.randint(1,1)
    print(res)
    # setup config
    #config_path = "../config-feedforward.txt"
    #config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                #neat.DefaultStagnation, config_path)

    # init NEAT
    #p = neat.Population(config)

    # run NEAT
    #p.run(run_generation, 1000)
