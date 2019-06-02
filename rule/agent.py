import threading
import time
from rule.hand_card import HandCard
from rule.player import Player
from rule.player_info import PlayerInfo
from rule.tenpai import *
from ai.dqn import DeepQNetwork
import numpy as np

class Agent:#(threading.Thread):

    id = 0
    def __init__(self, pai, info, id):
        #threading.Thread.__init__(self)
        
        self.card = pai
        self.info = info
        self.id = id
        self.new_s = -1

    def set_ai(self, name, new_model, epoch, batch_size, gamma, epsilon, in_dim = 1, middle_dim = 1, out_dim = 1, learning_rate = 0.001, training_action = 0):
        # name, new_model, epoch, batch_size, gamma, epsilon, in_dim = 1, middle_dim = 1, out_dim = 1, learning_rate = 0.001
        self.ai = DeepQNetwork(name, new_model, epoch, batch_size, gamma, epsilon, in_dim, middle_dim, out_dim, learning_rate, training_action)

    # return 0 or chi case
    def want_to_chi(self):
        # . . .
        #return self.info.chi_able_list[0][2]
        return 0

    def want_to_pon(self):
        # . . .
        return False

    def want_to_richi(self):
        # . . .
        return 1

    def want_to_kan(self):
        # . . .
        return False

    def want_to_ron(self):
        # . . .
        return True

    # return an kan case
    def want_to_ankan(self):
        # . . .
        return -1

    def want_to_tsumo(self):
        # . . .
        return True

    def which_to_discard(self):
        # . . .
        return self.ai.choose_action(self.get_state(), self.card)

    def run(self):
        if True:
        #while not self.info.end_game:
            if self.info.update_reward:
                self.ai.store_transition(0)
                self.ai.update_reward(self.calc_reward())
                self.info.update_reward = False
                self.info.reward = 0
                pass

            if self.info.time_to_discard:
                if self.info.can_richi:
                    self.info.want_to_richi = self.want_to_richi()
                if self.info.can_tsumo:
                    self.info.can_tsumo = False
                    if self.want_to_tsumo():
                        self.info.want_to_tsumo = True
                        return
                if self.info.can_ankan:
                    self.info.can_ankan = False
                    self.info.an_kan_case = self.want_to_ankan()
                    if self.info.an_kan_case != -1:
                        self.info.action_state = 2
                        return
                self.info.discard_tile = self.which_to_discard()
                self.ai.store_transition(0)
            else :
                if self.info.can_ron:
                    if self.want_to_ron():
                        self.info.action_state = 6
                    else :
                        self.info.action_state = 0
                    self.info.can_ron = False
                if self.info.can_kan:
                    if self.want_to_kan():
                        self.info.can_pon = False
                        self.info.can_kan = False
                        self.info.action_state = 2
                        return
                    else :
                        self.info.action_state = 0
                    self.info.can_kan = False
                if self.info.can_pon:
                    if self.want_to_pon():
                        self.info.action_state = 1
                    else :
                        self.info.action_state = 0
                    self.info.can_pon = False
                if self.info.can_chi:
                    self.info.action_state = self.want_to_chi()
                    self.info.can_chi = False

    def calc_reward(self):
        result = [0, 0, 0, 0]
        # calculate how many tile go get yaku
        # tan yao
        lenth = len(self.card.check_card14)
        tile_19_number = 0
        for i in range(lenth):
            if self.card.check_card14[lenth - i - 1] >= 30 or self.card.check_card14[lenth - i - 1] % 10 == 1 or self.card.check_card14[lenth - i - 1] % 10 == 9:
                tile_19_number += 1
        result[0] = tile_19_number
        # somete
        pin_number = 0
        man_number = 0
        sou_number = 0
        for i in self.card.check_card14:
            if i < 10:
                pin_number += 1
            elif i < 20:
                man_number += 1
            elif i < 30:
                sou_number += 1
        sum_number = sum([pin_number, man_number, sou_number])
        result[1] = sum_number - max([pin_number, man_number, sou_number])
        # kokushi
        card_19 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in self.card.check_card14:
            if i == 1 and card_19[0] == 0:
                card_19[0] += 1
            if i == 9 and card_19[1] == 0:
                card_19[1] += 1
            if i == 11 and card_19[2] == 0:
                card_19[2] += 1
            if i == 19 and card_19[3] == 0:
                card_19[3] += 1
            if i == 21 and card_19[4] == 0:
                card_19[4] += 1
            if i >= 29 and card_19[int(i) - 24] == 0:
                card_19[int(i) - 24] += 1
        result[2] = 13 - sum(card_19)
        # anko
        anko_number = 0
        pair_number = 0
        card = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in self.card.check_card14:
            card[int(i)] += 1
        for i in card:
            if i >= 3:
                anko_number += 1
            if i == 2:
                pair_number += 1
        result[3] = (4 - anko_number) * 2 - pair_number

        for i in range(4):
            if result[i] == 0:
                result[i] = 0.95
            if result[i] == 1:
                result[i] = 0.9
            if result[i] == 2:
                result[i] = 0.6
            if result[i] == 3:
                result[i] = 0.3
            if result[i] == 4:
                result[i] = 0.1
            if result[i] >= 5:
                result[i] = 0
            if result[i] == 0.95 and self.info.i_win:
                result[i] = 1
        self.info.i_win = False
        
        return result

    def old_get_state(self):
        arr = np.array([np.zeros(34)])
        card = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in self.card.check_card14:
            card[int(i)] += 1
            if i >= 30:
                arr[0][int(i) - 4] += 1
            elif i > 20:
                arr[0][int(i) - 3] += 1
            elif i > 10:
                arr[0][int(i) - 2] += 1
            else :
                arr[0][int(i) - 1] += 1
        return [arr, card]
    
    def get_state(self):
        card = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in self.card.check_card14:
            card[int(i)] += 1
        
        pair_number = 0         #7
        kotsu_number = 0        #5
        mentsu_19_number = 0    #5
        mentsu_28_number = 0    #5
        datsu_19_number = 0     #5
        datsu_28_number = 0     #5
        pin_number = 0          #15
        man_number = 0          #15
        sou_number = 0          #15
        tile_19_number = 0      #14

        for i in range(37):
            if i == 2:
                pair_number += 1
            if i >= 3:
                kotsu_number += 1

        for i in range(0, 10):
            pin_number += i
        for i in range(10, 20):
            man_number += i
        for i in range(20, 30):
            sou_number += i
        for i in range(37):
            if i == 1 and card[i] > 0:
                tile_19_number += 1
            if i == 9 and card[i] > 0:
                tile_19_number += 1
            if i == 11 and card[i] > 0:
                tile_19_number += 1
            if i == 19 and card[i] > 0:
                tile_19_number += 1
            if i == 21 and card[i] > 0:
                tile_19_number += 1
            if i >= 29 and card[i] > 0:
                tile_19_number += 1

        i = 1
        while True:
            if i > 36:
                break
            if card[i] > 0:
                if i < 28:
                    if card[i] > 0 and card[i + 1] > 0 and card[i + 2] > 0:
                        if i % 10 == 1 or i % 10 == 7:
                            mentsu_19_number += 1
                        else :
                            mentsu_28_number += 1
                        card[i] -= 1
                        card[i + 1] -= 1
                        card[i + 2] -= 1
                        continue
                    if card[i] > 2:
                        if i % 10 == 1 or i % 10 == 9:
                            mentsu_19_number += 1
                        else :
                            mentsu_28_number += 1
                        card[i] -= 3
                        continue
                else :
                    if card[i] > 2:
                        if i % 10 == 1 or i % 10 == 9:
                            mentsu_19_number += 1
                        else :
                            mentsu_28_number += 1
                        card[i] -= 3
                        continue
            i += 1

        i = 1
        while True:
            if i > 36:
                break
            if card[i] > 0:
                if i < 29:
                    if card[i] == 2:
                        if i % 10 == 1 or i % 10 == 9:
                            datsu_19_number += 1
                        else :
                            datsu_28_number += 1
                        card[i] -= 2
                        continue
                    if card[i] > 0 and card[i + 1] > 0:
                        if i % 10 == 1 or i % 10 == 8:
                            datsu_19_number += 1
                        else :
                            datsu_28_number += 1
                        card[i] -= 1
                        card[i + 1] -= 1
                        continue
                else :
                    if card[i] == 2:
                        if i % 10 == 1 or i % 10 == 9:
                            datsu_19_number += 1
                        else :
                            datsu_28_number += 1
                        card[i] -= 2
                        continue
            i += 1

        return np.array([[pair_number, kotsu_number, mentsu_19_number, mentsu_28_number, datsu_19_number, datsu_28_number, pin_number, man_number, sou_number, tile_19_number]])





if __name__ == '__main__':
    pl = Player()
    test = Agent(pl.card, pl.info)
    print("test ", test.card.card14)
    print("pl   ", pl.card.card14)
    pl.draw(19)
    print("test ", test.card.card14)
    print("pl   ", pl.card.card14)


