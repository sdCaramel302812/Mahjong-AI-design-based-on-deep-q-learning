import numpy as np
import json
from keras.initializers import normal, identity
from keras.models import model_from_json
from keras.models import Sequential
from keras.models import load_model
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.optimizers import SGD, Adam, RMSprop
import tensorflow as tf
import copy
import random

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 


class DeepQNetwork:
    def __init__(self, name, new_model, epoch, batch_size, gamma, epsilon, in_dim = 1, middle_dim = 1, out_dim = 1, learning_rate = 0.001):
        self.name = name
        self.epoch = epoch
        self.batch_size = batch_size
        self.gamma = gamma
        # epsilon for q learning, not for network
        self.epsilon = epsilon
        self.trasition = []
        self.start_k = 0
        self.old_state = []
        self.action = 0

        if new_model:
            opt = RMSprop(lr=learning_rate, rho=0.9, epsilon=1e-08, decay=0.0)
            self.eval_model = Sequential([Dense(middle_dim, input_dim = in_dim), Activation('relu'), Dense(out_dim), Activation('softmax')])
            self.eval_model.compile(loss='categorical_crossentropy',
                optimizer=opt,
                metrics=['accuracy'])

            self.target_model = Sequential([Dense(middle_dim, input_dim = in_dim), Activation('relu'), Dense(out_dim), Activation('softmax')])
            self.target_model.compile(loss='categorical_crossentropy',
                optimizer=opt,
                metrics=['accuracy'])
        else :
            file_name = self.name + '.h5'
            self.eval_model = load_model(file_name)
            self.target_model = load_model(file_name)

    def reset(self):
        self.trasition = []
        self.start_k = 0

    def choose_action(self, state, card14):
        decide_q = self.target_model.predict(state)
        self.old_state = state
        if np.random.uniform() < self.epsilon:
            rd = random.randint(0, len(card14) - 1)
            return card14[rd]
        else :
            while True:
                self.action = np.argmax(decide_q[0])
                if self.action in card14:
                    return self.action
                else :
                    decide_q[0][self.action] = 0

    # s : 向聽數
    def store_transition(self, reward, next_state, s):
        if self.old_state != []:
            self.trasition.append([self.old_state, self.action, reward, next_state, s])

    def update_reward(self, reward):
        self.old_state = []
        while self.start_k < len(self.trasition):
            self.trasition[self.start_k][2] += reward / (pow(self.trasition[self.start_k][4] + 1, 2) + 1)
            self.start_k += 1

    def train(self):
        minibatch = random.sample(self.trasition, self.batch_size)
        inputs = np.zeros((0, 34))
        targets = np.zeros((0, 34))
        for i in range(0, self.batch_size):
            state = minibatch[i][0]
            action = minibatch[i][1]
            reward = minibatch[i][2]
            next_state = minibatch[i][3]
            inputs = np.append(inputs, state, axis=0)
            targets = np.append(targets, self.target_model.predict(state), axis=0)

            if len(next_state) != 0:
                Q_sa = self.target_model.predict(next_state)
                targets[i, action] = reward + self.gamma * np.max(Q_sa[0])

            self.eval_model.fit(inputs, targets, epochs=self.epoch, batch_size=self.batch_size)



    def save_training(self):
        file_name = self.name + '.h5'
        self.target_model = copy.deepcopy(self.eval_model)
        self.target_model.save(file_name)



if __name__ == '__main__':
    test = DeepQNetwork( 'test_model', True, 1, 32, 0.5, 0.1, 3, 32, 3, 0.1)
    _input1 = np.array([[10,0,0]])#[[1,3,2,1,3],[1,2,3,2,3],[2,1,3,1,2],[1,2,1,1,3],[1,3,3,2,1],[1,3,2,3,1],[2,1,2,3,1],[1,3,2,2,3]]
    _input2 = np.array([[0,8,2]])
    for i in range(0, 100):
        if i % 2 == 0:
            _input1 = np.append(_input2, [[10,0,0]], axis=0)
        else :
            _input2 = np.append(_input1, [[0,8,2]], axis=0)

    _target1 = np.array([[1,0,0]])#[[1,0,0],[0,1,0],[0,1,0],[1,0,0],[1,0,0],[1,0,0],[0,1,0],[0,0,1]]
    _target2 = np.array([[0,0.8,0.2]])
    for i in range(0, 100):
        if i % 2 == 0:
            _target1 = np.append(_target2, [[1,0,0]], axis=0)
        else :
            _target2 = np.append(_target1, [[0,0.8,0.2]], axis=0)

    #test.target_model.fit(_input1, _target1, batch_size=1)
    #predict = test.target_model.predict(np.array([[0,8,2]]))
    #print(predict)
    eee[0] = 5
