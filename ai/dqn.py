import argparse
import numpy as numpy
import json
from keras.initializers import normal, identity
from keras.models import model_from_json
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.optimizers import SGD, Adam
import tensorflow as tf


class DeepQNetwork:
    test = 0
