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

    def set_ai(self, name, new_model, epoch, batch_size, gamma, epsilon, in_dim = 1, middle_dim = 1, out_dim = 1, learning_rate = 0.001):
        # name, new_model, epoch, batch_size, gamma, epsilon, in_dim = 1, middle_dim = 1, out_dim = 1, learning_rate = 0.001
        self.ai = DeepQNetwork(name, new_model, epoch, batch_size, gamma, epsilon, in_dim, middle_dim, out_dim, learning_rate)

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
        return False

    # return an kan case
    def want_to_ankan(self):
        # . . .
        return -1

    def want_to_tsumo(self):
        # . . .
        return True

    def which_to_discard(self):
        # . . .
        return self.ai.choose_action(self.get_state(), self.card.card14)

    def run(self):
        if True:
        #while not self.info.end_game:
            if self.info.update_reward:
                self.ai.store_transition(0, [], 0)
                self.ai.update_reward(self.info.reward)
                self.info.update_reward = False
                self.info.reward = 0
                pass

            if self.info.time_to_discard:
                if self.card.old_s == -1:
                    self.card.old_s = find_shan_ten_table(self.card, 14)
                else :
                    self.card.old_s = self.new_s
                    self.new_s = find_shan_ten_table(self.card, 14)
                    # reward, next_state, s
                    self.ai.store_transition(self.calc_reward(), self.get_state(), self.card.old_s)
                if self.info.can_richi:
                    self.info.want_to_richi = want_to_richi()
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
        diff = self.card.old_s - self.new_s
        return diff * 0.1

    def get_state(self):
        arr = np.array([np.zeros(34)])
        for i in self.card.check_card14:
            if i >= 30:
                arr[0][int(i) - 4] += 1
            elif i > 20:
                arr[0][int(i) - 3] += 1
            elif i > 10:
                arr[0][int(i) - 2] += 1
            else :
                arr[0][int(i) - 1] += 1
        return arr



if __name__ == '__main__':
    pl = Player()
    test = Agent(pl.card, pl.info)
    print("test ", test.card.card14)
    print("pl   ", pl.card.card14)
    pl.draw(19)
    print("test ", test.card.card14)
    print("pl   ", pl.card.card14)


