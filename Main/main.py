#from View.view import View
#from Game.game import Game
from Model.model import Model
from Controllers.mainController import Controller
from Net.actor import Actor
import random
import numpy as np
import neat
from Net.netProcessor import NetProcessor


if __name__ == "__main__":
    processor = NetProcessor()
    processor.run()
