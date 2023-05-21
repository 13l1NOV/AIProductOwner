import tensorflow as tf
from tensorflow.keras import initializers
import numpy as np
from Net.GameDoing import GameDoing

class DeepNet:
    def __init__(self):
        self.model = self.create_initial_net()
        self.fitness = 0
        self.count_backlog = 6
        self.count_tasks = 32

    def create_initial_net(self):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(12, activation='selu', kernel_initializer=tf.keras.initializers.RandomNormal(mean=0., stddev=1.)),
            #tf.keras.layers.BatchNormalization(),
            #tf.keras.layers.Dense(12, activation='selu', input_shape=(1,), kernel_initializer=tf.keras.initializers.RandomNormal(mean=0., stddev=1.)),
            tf.keras.layers.Dense(6, activation='selu', kernel_initializer=tf.keras.initializers.RandomNormal(mean=0., stddev=1.)),
            #tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dense(1)
        ])
        model.compile()
        #model.summary()
        #model.evaluate()
        return model

    def get_weights(self):
        layers = self.model.layers
        weights = []
        for layer in layers:
            layer_weights = layer.get_weights()
            weights.append(layer_weights[0])
            #if len(layer_weights) > 1:
            #    weights.append(layer_weights[1])
        return weights

    def replace_net_weight(self):
        #model.load_weights(...)
        pass

    def step(self, game_state):
        tensor = np.array([game_state])
        print(game_state)
        #tensor = tf.reshape(tensor, [1, 140])
        #res = self.model(tensor)
        #res = self.model.predict(game_state)
        res = self.model.predict(tensor)
        print("DeepNet_step ", res[0][0])
        #print(res)
        res_int = round(res[0][0])
        #res_int = round(tensor.numpy())
        if res_int < 0:
            return (GameDoing.RELEASE, None)
        if res_int == 0:
            return (GameDoing.SPRINT, None)
        if res_int == 1:
            return (GameDoing.DO_RESEARCH, None)
        if res_int == 2:
            return (GameDoing.DO_SURVEY, None)
        if 3 <= res_int < 3 + self.count_backlog:
            return (GameDoing.DECOMPOSE, res_int - 3)
        if 3 + self.count_backlog <= res_int and res_int < 3 + self.count_backlog + self.count_tasks:
            return (GameDoing.SELECT_TASK, res_int - 3 + self.count_backlog)
        if res_int >= 3 + self.count_backlog + self.count_tasks:
            return (GameDoing.BUY_ROBOT, None) # проверить что нормально вренется # проверено что нет

        raise NameError("bad state")