import tensorflow as tf
from tensorflow.keras import initializers

class DeepNet:
    def __init__(self):
        self.model = create_initial_net()
        self.fitness = 0
        self.count_backlog = 6
        self.count_tasks = 32

    def create_initial_net(self):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(12, activation='selu', input_shape=(53,), kernel_initializer=tf.keras.initializers.RandomNormal(mean=0., stddev=1.)),
            tf.keras.layers.Dense(6, activation='selu', kernel_initializer=tf.keras.initializers.RandomNormal(mean=0., stddev=1.)),
            tf.keras.layers.Dense(1)
        ])
        model.eval()
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
        pass

    def step(self, game_state):
        res = self.model(game_state)
        print("DeepNet_step ", res)
        res_int = round(res)
        if res_int < 0:
            return (GameDoing.RELEASE)
        if res_int == 0:
            return (GameDoing.SPRINT)
        if res_int == 1:
            return (GameDoing.DO_RESEARCH)
        if res_int == 2:
            return (GameDoing.DO_SURVEY)
        if res_int == 2:
            return (GameDoing.DO_SURVEY)
        if 3 <= res_int < 3 + self.count_backlog:
            return (GameDoing.DECOMPOSE, res_int - 3)
        if 3 + self.count_backlog <= res_int and res_int < 3 + self.count_backlog + self.count_tasks:
            return (GameDoing.SELECT_TASK, res_int - 3 + self.count_backlog)
        if res_int <= 3 + self.count_backlog + self.count_tasks:
            return (GameDoing.BUY_ROBOT) # проверить что нормально вренется

        raise NameError("bad state")