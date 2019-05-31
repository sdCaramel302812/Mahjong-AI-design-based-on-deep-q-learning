from rule.hand_card import HandCard
import numpy as np
from rule.tenpai import *
from rule.player_info import PlayerInfo
import copy

class Player:
    id = 0
    def __init__(self):
        self.card = HandCard()
        self.info = PlayerInfo()
        self.reset()

    def reset(self):
        self.info.i_ba_tsu = False
        self.info.first = True
        self.info.fu_ri_ten = False
        self.info.discard_tile = -1
        self.info.action_state = -1
        self.card.reset()
        self.info.rin_shan = False
        self.info.chan_kan = 0
        self.info.update_reward = True

    def new_game(self, id):
        self.id = id
        self.info.point = 25000

    def can_do_something(self, pai, left_hand, dora):
        if not self.card.richi:
            pai_no_r = pai
            if pai_no_r == 0 or pai_no_r == 10 or pai_no_r == 20:
                pai_no_r += 5
            
            self.info.can_do_something = False
            #check can chi or not
            self.info.chi_able_list = []
            self.info.can_chi = False
            if left_hand and pai_no_r < 30 and len(self.card.card13) > 2:
                # pai - 2, pai - 1, pai + 1, pai + 2
                has_tile = [False, False, False, False]

                for i in self.card.check_card13:
                    if i >= 30:
                        continue
                    if pai_no_r % 10 != 1:
                        if pai_no_r - i == 2:
                            has_tile[0] = True
                        if pai_no_r - i == 1:
                            has_tile[1] = True
                    if pai_no_r % 10 != 9:
                        if i - pai_no_r == 1:
                            has_tile[2] = True
                        if i - pai_no_r == 2:
                            has_tile[3] = True
                if has_tile[0] and has_tile[1]:
                    self.info.can_chi = True
                    self.info.chi_able_list.append([pai_no_r - 2, pai_no_r - 1, 5])
                if has_tile[1] and has_tile[2]:
                    self.info.can_chi = True
                    self.info.chi_able_list.append([pai_no_r - 1, pai_no_r + 1, 4])
                if has_tile[2] and has_tile[3]:
                    self.info.can_chi = True
                    self.info.chi_able_list.append([pai_no_r + 1, pai_no_r + 2, 3])
            #check can pon or not
            self.info.pon_able_tile = -1
            self.info.can_pon = False
            self.info.can_kan = False
            same_num = 0
            for i in self.card.check_card13:
                if pai_no_r == i:
                    same_num += 1
            if same_num >= 2:
                self.info.can_pon = True
                pon_able_tile = pai_no_r
                self.info.pon_able_tile = pai_no_r
            if same_num >= 3:
                self.info.can_kan = True
        #check can ron or not
        self.card.ron(pai)
        self.info.can_ron = False
        if win_check(self.card) and not self.info.fu_ri_ten:
            yaku = point_check(self.card, self.info.chan_fon, self.info.men_fon, self.info.last, self.info.first, self.info.rin_shan, self.info.chan_kan, self.info.i_ba_tsu, 0, dora, [])
            if not yaku.yaku_nashi:
                self.info.can_ron = True
        
        if self.info.can_chi or self.info.can_kan or self.info.can_pon or self.info.can_ron:
            self.info.can_do_something = True
            return True
        else :
            self.info.can_do_something = False
            return False




    def draw(self, p):
        self.card.draw(p)
        self.info.time_to_discard = True

    def discard(self, discard_stack):
        if self.info.discard_tile != -1:
            for i in range(int(len(self.info.what_to_tenpai) / 2)):
                if self.info.discard_tile == self.info.what_to_tenpai[i * 2][0]:
                    self.info.tenpai_list = copy.copy(self.info.what_to_tenpai[i * 2][1])
            if len(self.info.what_to_tenpai) == 0 and not self.card.richi:
                self.info.tenpai_list = []
            self.info.what_to_tenpai = []

            if self.info.want_to_richi == 1:
                self.card.richi = True
                self.info.i_ba_tsu = True
                self.info.want_to_richi = 0
                self.info.can_richi = False
                self.info.point -= 1000
            p = self.info.discard_tile
            self.card.discard(p)
            self.info.time_to_discard = False
            self.info.discard_tile = -1
            self.fu_ri_ten_check(discard_stack)
            return p
        else :
            return -1

    def an_kan(self):
        if self.info.action_state == 2:
            self.info.action_state = -1
            if len(self.info.kan_able_list) <= self.info.an_kan_case:
                return [0, 0]
            ka_kan = self.info.kan_able_list[self.info.an_kan_case][1]
            kan_pai = self.info.kan_able_list[self.info.an_kan_case][0]
            if ka_kan == 1:
                self.card.ka_kan(kan_pai)
            else :
                self.card.an_kan(kan_pai)
            self.info.an_kan_case = -1
            self.info.kan_able_list = []
            self.info.time_to_discard = False
            self.info.can_ankan = False
            return [ka_kan, kan_pai]

        else :
            return [0, 0]

    def tsumo(self):
        if self.info.want_to_tsumo:
            self.info.want_to_tsumo = False
            return True
        return False

    # naki
    def claim(self, pai):
        if not self.info.can_do_something:
            return 0

        if self.info.action_state > 0 and self.info.action_state != 2:
            self.info.just_naki = True
        return self.info.action_state

    def be_claimed(self):
        self.info.i_ba_tsu = False
        self.info.first = False

    def fu_ri_ten_check(self, discard_stack):
        if not self.card.richi:
            self.info.fu_ri_ten = False
        for i in self.info.tenpai_list:
            for j in discard_stack:
                p = j
                if p == 0 or p == 10 or p == 20:
                    p += 5
                if p == i:
                    self.info.fu_ri_ten = True
                    break

    def can_chan_kan(self, ron_pai, kan):
        if self.info.has_tenpai:
            # kan  1 : kakan
            # kan -1 : ankan
            if kan == 1:
                for i in self.info.tenpai_list:
                    if i == ron_pai:
                        self.info.can_ron = True
                        return True
            elif kan == -1:
                for i in self.info.tenpai_list:
                    if i == ron_pai:
                        self.card.ron(ron_pai)
                        if kokushi_check(self.card):
                            self.info.can_ron = True
                            return True
                        return False
        return False

    def an_kan_tsumo_check(self):
        if win_check(self.card):
            yaku = point_check(self.card, self.info.chan_fon, self.info.men_fon, self.info.last, self.info.first, self.info.rin_shan, self.info.chan_kan, self.info.i_ba_tsu, 0, [], [])
            if not yaku.yaku_nashi:
                self.info.can_can_tsumo = True
        else :
            self.info.what_to_tenpai = richi_check(self.card)
            if len(self.info.what_to_tenpai) != 0 and len(self.card.chi_card) == 0 and len(self.card.pon_card) == 0:
                men_zen = True
                for i in self.card.kan_card:
                    if i[1] != 0:
                        men_zen = False
                if men_zen and self.info.point >= 1000:
                    self.info.can_richi = True

        pin = np.zeros(9)
        man = np.zeros(9)
        sou = np.zeros(9)
        other = np.zeros(7)
        for i in self.card.check_card14:
            if i >= 30:
                other[int(i) - 30] += 1
            elif i > 20:
                sou[int(i) - 21] += 1
            elif i > 10:
                man[int(i) - 11] += 1
            else :
                pin[int(i) - 1] += 1
            
        self.info.kan_able_list = []
        for i in range(0, 9):
            if pin[i] == 4:
                self.info.kan_able_list.append([i + 1, -1])
                self.info.can_ankan = True
            if man[i] == 4:
                self.info.kan_able_list.append([i + 11, -1])
                self.info.can_ankan = True
            if sou[i] == 4:
                self.info.kan_able_list.append([i + 21, -1])
                self.info.can_ankan = True
        for i in range(0, 7):
            if other[i] == 4:
                self.info.kan_able_list.append([i + 30, -1])
                self.info.can_ankan = True

        for i in self.card.pon_card:
            for j in self.card.check_card14:
                if i[2] == j:
                    self.info.kan_able_list.append([i, 1])
                    self.info.can_ankan = True

        if self.info.just_naki:
            self.info.can_ankan = False
        self.info.just_naki = False







if __name__ == '__main__':
    pl = Player()
    pl.draw(18)
    pl.info.discard_tile = 10
    pl.can_do_something(3, True, [])
    pl.discard()
    print(pl.card.card14)

