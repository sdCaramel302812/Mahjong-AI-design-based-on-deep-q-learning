import numpy as np
import json
from keras.initializers import normal, identity
from keras.models import model_from_json
from keras.models import Sequential
from keras.models import load_model
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.optimizers import SGD, Adam, RMSprop
from keras.callbacks import ModelCheckpoint
import tensorflow as tf
import copy
import random
from rule.tenpai import find_effective_table, find_shan_ten_table
import time

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 


class DeepQNetwork:
    def __init__(self, name, new_model, epoch, batch_size, gamma, epsilon, in_dim = 1, middle_dim = 1, out_dim = 1, learning_rate = 0.001, training_action = 0):
        self.name = name
        self.epoch = epoch
        self.batch_size = batch_size
        self.gamma = gamma
        # epsilon for q learning, not for network
        self.epsilon = epsilon
        self.trasition = []
        self.start_k = 0
        self.old_state = []
        self.action = training_action
        self.training_action = training_action

        if new_model:
            file_name = self.name + '.h5'
            opt = RMSprop(lr=learning_rate, rho=0.9, epsilon=1e-08, decay=0.0)
            self.model = Sequential([Dense(middle_dim, input_dim = in_dim), Activation('relu'), Dense(out_dim), Activation('softmax')])
            self.model.compile(loss='categorical_crossentropy',
                optimizer=opt,
                metrics=['accuracy'])
            check_point = ModelCheckpoint(file_name, monitor='val_loss', verbose=0, save_best_only=False, save_weights_only=False, mode='auto', period=1)
            self.callbacks_list = [check_point]
        else :
            file_name = self.name + '.h5'
            opt = RMSprop(lr=learning_rate, rho=0.9, epsilon=1e-08, decay=0.0)
            self.model = load_model(file_name)
            self.model.compile(loss='categorical_crossentropy',
                optimizer=opt,
                metrics=['accuracy'])
            check_point = ModelCheckpoint(file_name, monitor='val_loss', verbose=0, save_best_only=False, save_weights_only=False, mode='auto', period=1)
            self.callbacks_list = [check_point]


    def reset(self):
        self.trasition.clear()
        self.start_k = 0

    def choose_action(self, state, card):
        self.old_state = state
        if self.training_action == -1:
            decide_q = self.model.predict(state)
            self.action = np.argmax(decide_q[0])
        if self.action == 0:
            return self.default_action(card)
        elif self.action == 1:
            tile = self.tan_yao_action(card)
            if tile == -1:
                return self.default_action(card)
            else :
                return tile
        elif self.action == 2:
            tile = self.somete_action(card)
            if tile == -1:
                return self.default_action(card)
            else :
                return tile
        elif self.action == 3:
            tile = self.kokushi_action(card)
            if tile == -1:
                return self.default_action(card)
            else :
                return tile
        elif self.action == 4:
            tile = self.an_ko_action(card)
            if tile == -1:
                return self.default_action(card)
            else :
                return tile
        

        '''
        self.old_state = state
        if np.random.uniform() < self.epsilon:
            rd = random.randint(0, len(card.card14) - 1)
            return card.card14[rd]
        else :
            while True:
                self.action = np.argmax(decide_q[0])
                if self.action in card.card14:
                    return self.action
                else :
                    decide_q[0][self.action] = 0
        '''

    # s : 向聽數
    def store_transition(self, reward):
        if self.old_state != []:
            self.trasition.append([self.old_state, self.action, reward])

    def update_reward(self, reward):
        self.old_state = []
        while self.start_k < len(self.trasition):
            self.trasition[self.start_k][2] += reward[self.trasition[self.start_k][1] - 1]
            self.start_k += 1

    def train(self):
        minibatch = random.sample(self.trasition, self.batch_size)
        inputs = np.zeros((0, 10))
        targets = np.zeros((0, 5))
        for i in range(0, self.batch_size):
            state = minibatch[i][0]
            action = minibatch[i][1]
            reward = minibatch[i][2]
            inputs = np.append(inputs, state, axis=0)
            targets = np.append(targets, self.model.predict(state), axis=0)

            targets[i, action] = reward
            targets[i, 0] = 1 - reward

            self.model.fit(inputs, targets, epochs=self.epoch, batch_size=self.batch_size, callbacks=self.callbacks_list)



    def save_training(self):
        file_name = self.name + '.h5'
        #self.target_model = copy.deepcopy(self.eval_model)
        #self.target_model.save(file_name)
        ModelCheckpoint(file_name, monitor='val_loss', verbose=0, save_best_only=False, save_weights_only=False, mode='auto', period=1)

    def default_action(self, card):
        s = find_shan_ten_table(card, 14)
        back_up = copy.deepcopy(card)
        choose_table = {}

        state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in card.check_card14:
            state[int(i)] += 1
            
        for i in range(1, 37):
            if state[i] > 0:
                back_up.discard(i)
                next_s = find_shan_ten_table(back_up)
                if next_s == s:
                    state[i] -= 1
                    choose_table[i] = find_effective_table(state)
                    state[i] += 1
                back_up.draw(i)
        
        max_number = 0
        max_index = 0
        has_find_action = False
        for key, value in choose_table.items():
            if value > max_number:
                has_find_action = True
                max_number = value
                max_index = key
        if has_find_action:
            return max_index
        else :
            return card.card14[-1]

    def tan_yao_action(self, card):
        lenth = len(card.check_card14)
        for i in range(lenth):
            if card.check_card14[lenth - i - 1] >= 30 or card.check_card14[lenth - i - 1] % 10 == 1 or card.check_card14[lenth - i - 1] % 10 == 9:
                return card.check_card14[lenth - i - 1]
        return -1

    def somete_action(self, card):
        pin_number = 0
        man_number = 0
        sou_number = 0
        for i in card.check_card14:
            if i < 10:
                pin_number += 1
            elif i < 20:
                man_number += 1
            elif i < 30:
                sou_number += 1
        max_color = np.argmax(np.array([pin_number, man_number, sou_number]))
        if max_color == 0:
            for i in card.check_card14:
                if i > 10:
                    return i
        if max_color == 1:
            for i in card.check_card14:
                if i < 10 or i > 20:
                    return i
        if max_color == 2:
            for i in card.check_card14:
                if i < 20:
                    return i
        return -1

    def kokushi_action(self, card):
        card_19 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in card.check_card14:
            if i == 1:
                card_19[0] += 1
            if i == 9:
                card_19[1] += 1
            if i == 11:
                card_19[2] += 1
            if i == 19:
                card_19[3] += 1
            if i == 21:
                card_19[4] += 1
            if i >= 29:
                card_19[int(i) - 24] += 1
            if i < 30:
                if i % 10 > 1 and i % 10 < 9:
                    return i
        
        for i in range(13):
            has_pair = False
            if card_19[i] > 2 or (card_19[i] == 2 and has_pair):
                if i == 0:
                    return 1
                if i == 1:
                    return 9
                if i == 2:
                    return 11
                if i == 3:
                    return 19
                if i == 4:
                    return 21
                if i >= 5:
                    return 24 + i
            if card_19[i] == 2:
                has_pair = True
        return -1

    def an_ko_action(self, card):
        pin = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        man = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        sou = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        other = [0, 0, 0, 0, 0, 0, 0]
        for i in card.check_card14:
            if i < 10:
                pin[int(i) - 1] += 1
            elif i < 20:
                man[int(i) - 11] += 1
            elif i < 30:
                sou[int(i) - 21] += 1
            else :
                other[int(i) - 30] += 1
        for i in range(1, 8):
            if pin[i] == 1 and pin[i - 1] == 0 and pin[i + 1] == 0:
                return i + 1
            if man[i] == 1 and man[i - 1] == 0 and man[i + 1] == 0:
                return i + 11
            if sou[i] == 1 and sou[i - 1] == 0 and sou[i + 1] == 0:
                return i + 21
            if i < 7 and other[i] == 1:
                return i + 30
        if pin[0] == 1 and pin[1] == 0:
            return 1
        if man[0] == 1 and man[1] == 0:
            return 11
        if sou[0] == 1 and sou[1] == 0:
            return 21
        if pin[8] == 1 and pin[7] == 0:
            return 9
        if man[8] == 1 and man[7] == 0:
            return 19
        if sou[8] == 1 and sou[7] == 0:
            return 29
        for i in range(9):
            if pin[i] == 1:
                return i + 1
            if man[i] == 1:
                return i + 11
            if sou[i] == 1:
                return i + 21

        return -1
            





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
