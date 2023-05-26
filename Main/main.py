from Net.netProcessor import NetProcessor
import tensorflow as tf
from Net.Game import Game
# from Net.DeepNet import DeepNet
from Net import debug, DeepNet
from tensorflow import keras


def formatDoing(do, index):
    return (do.value, ("" if index == None else str(index)))


def net_step(net, game):
    state = game.get_state()
    do, index = net.step(state)
    game.execute(do, index)
    return (do, index)


def test_game(path):
    load_model = keras.models.load_model(path + '/saved_model/', custom_objects={'custom_loss': DeepNet.custom_loss})
    weights = load_model.get_weights()
    load_net = DeepNet.DeepNet()
    load_net.replace_net_weight(weights)
    game = Game()
    net_doings = []
    for iteration in range(10):
        do, index = net_step(load_net, game)
        net_doings.append(formatDoing(do, index))
        print("------iteration " + str(iteration) + " ------")
        debug.status_bar(game.model)
        debug.status_office(game.model)
        debug.status_task(game.model)
        debug.status_subtask(game.model)

    print(net_doings)


if __name__ == "__main__":
    path = 'C:/Users/sever/Desktop'
    count_net = 40
    generations = 100
    iterations = 1000
    count_top_net = 20
    count_elitism_net = 2
    count_child_net = 10
    count_w_mutant = 4
    count_s_mutant = 4

    processor = NetProcessor(count_net, count_top_net, count_child_net, count_w_mutant, count_s_mutant)
    processor.run(generations, iterations, path)

    test_game(path)
